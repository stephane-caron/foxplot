#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Series data unpacked from input dictionaries."""

import typing
from dataclasses import dataclass
from typing import Any, Dict, List

from .decoders.json import decode_json
from .exceptions import FoxplotException


@dataclass
class SeriesValue:

    data: Dict[int, Any]
    label: str

    def __init__(self, label: str):
        self.data = {}
        self.label = label

    def get(self, index: int, default: Any):
        return self.data.get(index, default)

    def get_range(self, start, stop):
        return [self.get(index, None) for index in range(start, stop)]

    def update(self, index: int, value: Any):
        self.data[index] = value

    def __repr__(self):
        values = list(self.data.values())
        return f"Time series with values: {values}"


class NestedDict:
    """Series data unpacked from input dictionaries."""

    __label: str

    def __init__(self, label: str):
        self.__label = label

    def update(self, index: int, unpacked: dict) -> None:
        for key, value in unpacked.items():
            if key in self.__dict__:
                child = self.__dict__[key]
            else:  # key not in self.__dict__
                sep = "/" if not self.__label.endswith("/") else ""
                child = (
                    NestedDict if isinstance(value, dict) else SeriesValue
                )(label=f"{self.__label}{sep}{key}")
                self.__dict__[key] = child
            child.update(index, value)

    def get_from_keys(self, keys: List[str]) -> SeriesValue:
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child.get_from_keys(keys[1:])
        if not isinstance(child, SeriesValue):
            raise FoxplotException(f"{child.label} is not a time series")
        return child

    def __repr__(self):
        return "Dictionary with keys:\n- " + "\n- ".join(
            key for key in self.__dict__.keys() if not key.startswith("_")
        )


class Series:

    root: NestedDict

    def __init__(self):
        self.length = 0
        self.root = NestedDict("/")

    def read_from_file(self, file: typing.TextIO) -> None:
        """Process time series data.

        Args:
            file: File to read time series from.
        """
        for unpacked in decode_json(file=file):
            self.root.update(self.length, unpacked)
            self.length += 1

    def get(self, name: str) -> SeriesValue:
        keys = name.strip("/").split("/")
        return self.root.get_from_keys(keys)
