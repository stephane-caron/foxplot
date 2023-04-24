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

import webbrowser
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TextIO, Union

from .decoders.json import decode_json
from .exceptions import FoxplotException
from .generate_html import generate_html
from .plot import write_output


@dataclass
class SeriesValue:
    data: Dict[int, Any]
    label: str

    def __init__(self, label: str):
        self.data = {}
        self.label = label

    def _get(self, max_index: int):
        return [self.data.get(index, None) for index in range(max_index)]

    def _update(self, index: int, value: Any):
        self.data[index] = value

    def __repr__(self):
        values = list(self.data.values())
        return f"Time series with values: {values}"


class NestedDict:
    """Series data unpacked from input dictionaries."""

    __label: str

    def __init__(self, label: str):
        self.__label = label

    def _update(self, index: int, unpacked: Union[dict, list]) -> None:
        items = (
            unpacked.items()
            if isinstance(unpacked, dict)
            else enumerate(unpacked)
        )
        for key, value in items:
            if key in self.__dict__:
                child = self.__dict__[key]
            else:  # key not in self.__dict__
                sep = "/" if not self.__label.endswith("/") else ""
                child = (
                    NestedDict
                    if isinstance(value, (dict, list))
                    else SeriesValue
                )(label=f"{self.__label}{sep}{key}")
                self.__dict__[key] = child
            child._update(index, value)

    def _get_from_keys(self, keys: List[str]) -> SeriesValue:
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child._get_from_keys(keys[1:])
        if not isinstance(child, SeriesValue):
            raise FoxplotException(f"{child.label} is not a time series")
        return child

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        keys = ", ".join(
            str(key)
            for key in self.__dict__.keys()
            if isinstance(key, int) or not key.startswith("_")
        )
        return f"{self.__label}: [{keys}]"


class Series:
    data: NestedDict
    time: str

    def __init__(self, time: str):
        """Initialize series.

        Args:
            time: Label of time index in input dictionaries.
        """
        self.length = 0
        self.data = NestedDict("/")
        self.time = time

    def read_from_file(self, file: TextIO) -> None:
        """Process time series data.

        Args:
            file: File to read time series from.
        """
        for unpacked in decode_json(file=file):
            self.data._update(self.length, unpacked)
            self.length += 1

    def get(self, label: str) -> SeriesValue:
        keys = label.strip("/").split("/")
        return self.data._get_from_keys(keys)

    def plot(
        self,
        left: List[SeriesValue],
        right: Optional[List[SeriesValue]] = None,
        title: str = "",
        left_axis_unit: str = "",
        right_axis_unit: str = "",
    ):
        times = (
            self.get(self.time)
            if self.time is not None
            else [float(x) for x in range(self.length)]
        )
        left_series = {
            series.label: series._get(self.length) for series in left
        }
        right_series = {
            series.label: series._get(self.length)
            for series in (right if right is not None else [])
        }
        html = generate_html(
            times,
            left_series,
            right_series,
            title,
            left_axis_unit,
            right_axis_unit,
            timestamped=self.time is not None,
        )
        filename = write_output(html)
        webbrowser.open_new_tab(filename)
