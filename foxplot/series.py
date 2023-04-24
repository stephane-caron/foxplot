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

    def read_from_file(self, file: typing.TextIO, start_index: int = 0) -> int:
        """Process time series data.

        Args:
            file: File to read time series from.
            start_index: Optional internal start index.

        Returns:
            Index after input has been read.
        """
        index = start_index
        print(f"read from {file=}")
        for unpacked in decode_json(file=file):
            self.update(index, unpacked)
            index += 1
        return index

    def update(self, index: int, unpacked: dict) -> None:
        for key, value in unpacked.items():
            if key in self.__dict__:
                child = self.__dict__[key]
            else:  # key not in self.__dict__
                child = (
                    NestedDict() if isinstance(value, dict) else SeriesValue()
                )
                self.__dict__[key] = child
            child.update(index, value)

    def __repr__(self):
        return "Dictionary with keys:\n- " + "\n- ".join(self.__dict__.keys())

    def _get_from_keys(self, keys: List[str], max_index: int):
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child._get_from_keys(keys[1:], max_index)
        return [child.get(index) for index in range(max_index)]

    def get_series(self, name: str, max_index: int):
        keys = name.strip("/").split("/")
        return self._get_from_keys(keys, max_index)
