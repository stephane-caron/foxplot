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

from typing import Any, Dict, List


class Series:
    """Indexed time-series values.

    Internally, this datastructure maps time indexes (the corresponding times
    themselves are stored in a different list) to values.
    """

    __data: Dict[int, Any]
    __label: str

    def __init__(self, label: str):
        """Initialize a new indexed series.

        Args:
            label: Label of the series in the input data.
        """
        self.__data = {}
        self.__label = label

    @property
    def _label(self) -> str:
        """Label of the series in the input data."""
        return self.__label

    def __len__(self):
        """Length of the indexed series."""
        return len(self.__data)

    def __repr__(self):
        """String representation of the series."""
        values = list(self.__data.values())
        return f"Time series with values: {values}"

    def _get(self, max_index: int):
        """Get indexed series as a list of values.

        Args:
            max_index: The output list will range from 0 (first time from the
                input) to this maximum index (excluded).

        Returns:
            Indexed series as a list of values.
        """
        last_value = None
        values = []
        for index in range(max_index):
            last_value = self.__data.get(index, last_value)
            values.append(last_value)
        return values

    def _list_labels(self) -> List[str]:
        """List all labels reachable from this node.

        Returns:
            List of labels. Since this node is a leaf, there is only one.
        """
        return [self.__label]

    def _update(self, index: int, value: Any) -> None:
        """Update the value at a given time index.

        Args:
            index: Time index.
            value: New value.
        """
        self.__data[index] = value
