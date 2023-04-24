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

from typing import Any, Dict, List, Union

from .exceptions import FoxplotException


class SeriesValue:
    """Indexed time-series values."""

    __data: Dict[int, Any]
    __label: str

    @property
    def label(self) -> str:
        """Label of the series in the input data."""
        return self.__label

    def __init__(self, label: str):
        self.__data = {}
        self.__label = label

    def __repr__(self):
        values = list(self.__data.values())
        return f"Time series with values: {values}"

    def _get(self, max_index: int):
        return [self.__data.get(index, None) for index in range(max_index)]

    def _list_labels(self) -> List[str]:
        return [self.__label]

    def _update(self, index: int, value: Any):
        self.__data[index] = value


class NestedDict:
    """Series data unpacked from input dictionaries."""

    __label: str

    def __init__(self, label: str):
        self.__label = label

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        keys = ", ".join(
            str(key)
            for key in self.__dict__.keys()
            if isinstance(key, int) or not key.startswith("_")
        )
        return f"{self.__label}: [{keys}]"

    def _get_child(self, keys: List[str]) -> SeriesValue:
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child._get_child(keys[1:])
        if not isinstance(child, SeriesValue):
            raise FoxplotException(f"{child.label} is not a time series")
        return child

    def _list_labels(self) -> List[str]:
        labels = []
        for key, child in self.__dict__.items():
            if isinstance(key, int) or key.startswith("_"):
                continue
            labels.extend(child._list_labels())
        return labels

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
