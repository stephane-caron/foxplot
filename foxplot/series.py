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
from typing import Any, Dict, List, Optional, Sequence, Union

from .decoders.json import decode_json


def get_from_keys(
    collection: Union[Dict[str, Any], List[Any]],
    keys: Sequence[str],
):
    """Get value from a nested dictionary.

    Get value `collection[key1][key2][...][keyN]` from a nested dictionary
    `collection` and keys `[key1, key2, ..., keyN]`.

    Args:
        collection: Dictionary or list to get value from.
        keys: Sequence of keys to the value.
    """
    key = keys[0]
    subcollection = (
        collection[int(key)]
        if isinstance(collection, list)
        else collection[key]
    )
    if len(keys) > 1:
        return get_from_keys(subcollection, keys[1:])
    return subcollection  # found a value


class Series:
    """Series data unpacked from input dictionaries.

    Attributes:
        fields: Fields to plot.
        field_values: Values for fields unpacked from input dictionaries.
        index_values: Index values, either generated or unpacked from input
            dictionaries.
        index: If set, read index values from input dictionaries.
        left_axis_fields: Fields to plot on the left axis.
        right_axis_fields: Fields to plot on the right axis.
        timestamped: If true, assume index is a Unix timestamp.
    """

    fields: List[str]
    field_values: Dict[str, Any]
    index_values: list
    index: Optional[str]
    left_axis_fields: List[str]
    right_axis_fields: List[str]
    timestamped: bool

    def __init__(
        self,
        index: Optional[str],
        left_axis_fields: List[str],
        right_axis_fields: List[str],
        timestamped: bool,
    ):
        """Initialize series data."""
        self.field_values = {}
        self.fields = left_axis_fields + right_axis_fields
        self.index = index
        self.index_values = []
        self.left_axis_fields = left_axis_fields
        self.right_axis_fields = right_axis_fields
        self.timestamped = timestamped

    def __unpack_value(self, unpacked: dict, field: str):
        try:
            keys = field.lstrip("/").split("/")
            value = get_from_keys(unpacked, keys)
        except KeyError as key_error:
            value = "null"
            if field == self.index:
                raise ValueError(
                    f'Index "{field}" undefined '
                    f"in unpacked item {unpacked}"
                ) from key_error
        return value

    def read_from_file(self, file: typing.TextIO) -> None:
        """Process time series data.

        Args:
            file: File to read time series from.

        Returns:
            Series data as a dictionary.
        """
        if len(self.fields) < 1:
            self.fields = ["/"]  # special field to expand all
        self.field_values = {field: [] for field in self.fields}
        nb_unpacked = 0
        for unpacked in decode_json(file=file):
            if self.index is None:
                self.index_values.append(nb_unpacked)
            else:  # self.index is not None:
                self.index_values.append(
                    self.__unpack_value(unpacked, self.index)
                )
            nb_unpacked += 1
            for field in self.fields:
                value = self.__unpack_value(unpacked, field)
                self.field_values[field].append(value)
        print(f"{self.index_values=}")
        print(f"{self.field_values=}")
