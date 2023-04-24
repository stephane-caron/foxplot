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
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .decoders.json import decode_json


@dataclass
class SeriesValue:

    data: Dict[int, Any] = field(default_factory=dict)

    def update(self, index: int, value: Any):
        self.data[index] = value

    def get(self, index: int):
        return self.data.get(index, None)

    def __repr__(self):
        values = list(self.data.values())
        return f"Time series with values: {values}"


class NestedDict:
    """Series data unpacked from input dictionaries."""

    label: str

    def __init__(self, label: str):
        self.label = label

    def update(self, index: int, unpacked: dict) -> None:
        for key, value in unpacked.items():
            if key in self.__dict__:
                child = self.__dict__[key]
            else:  # key not in self.__dict__
                sep = "/" if not self.label.endswith("/") else ""
                child = (
                    NestedDict(label=f"{self.label}{sep}{key}")
                    if isinstance(value, dict)
                    else SeriesValue()
                )
                self.__dict__[key] = child
            child.update(index, value)

    def __repr__(self):
        return "Dictionary with keys:\n- " + "\n- ".join(self.__dict__.keys())

    def get_from_keys(self, keys: List[str], max_index: int):
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child.get_from_keys(keys[1:], max_index)
        return [child.get(index) for index in range(max_index)]


class Series:

    index: int
    root: NestedDict

    def __init__(self):
        self.index = 0
        self.root = NestedDict("/")

    def read_from_file(self, file: typing.TextIO):
        """Process time series data.

        Args:
            file: File to read time series from.

        Returns:
            Index after input has been read.
        """
        for unpacked in decode_json(file=file):
            self.root.update(self.index, unpacked)
            self.index += 1

    def get(self, name: str):
        keys = name.strip("/").split("/")
        return self.root.get_from_keys(keys, self.index)
