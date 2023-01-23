#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

"""Command-line entry point for foxplot."""

import argparse
import sys
import tempfile
import typing
import webbrowser
from datetime import datetime
from os import path
from typing import Any, Dict, List, Optional, Sequence, Union

from .color_picker import ColorPicker
from .decoders.json import decode_json
from .exceptions import FieldNeedsExpansion
from .generate_html import generate_html
from .spdlog import logging


def parse_command_line_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", default=None)
    parser.add_argument(
        "-l",
        "--left",
        nargs="*",
        help="fields to plot using the (default) left axis",
    )
    parser.add_argument(
        "-lu",
        "--left-axis-unit",
        dest="left_axis_unit",
        default="",
        help="unit label for the left axis (default: empty)",
    )
    parser.add_argument(
        "-i",
        "--index",
        default=None,
        help="key to use as index for the time series (count items otherwise)",
    )
    parser.add_argument(
        "-r",
        "--right",
        nargs="*",
        help="fields to plot using the right axis",
    )
    parser.add_argument(
        "-ru",
        "--right-axis-unit",
        dest="right_axis_unit",
        default="",
        help="unit label for the right axis (default: empty)",
    )
    parser.add_argument(
        "-t",
        "--time",
        default="time",
        help="same as --index, but assume the key is a Unix time in seconds",
    )
    parser.add_argument(
        "--title",
        default=f"Plot from {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}",
        dest="title",
        help="plot title",
    )
    return parser.parse_args()


def get_fields(data: dict) -> List[str]:
    """Get the list of fields available in a nested dictionary.

    Returns:
        List of fields available in dictionary.
    """
    if not isinstance(data, dict):
        return []
    fields = []
    for key in data:
        if not isinstance(data[key], dict):
            fields.append(key)
        fields.extend(path.join(key, field) for field in get_fields(data[key]))
    return fields


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
    if isinstance(subcollection, dict):
        raise FieldNeedsExpansion(list(subcollection.keys()))
    if isinstance(subcollection, list):
        raise FieldNeedsExpansion(range(len(subcollection)))
    return subcollection  # found a value


def read_series(
    file: typing.TextIO,
    index: Optional[str],
    series_fields: List[str],
    left_axis_fields: List[str],
    right_axis_fields: List[str],
) -> Dict[str, list]:
    """Process time series data.

    Args:
        file: File to read time series from.
        index: Key to use as index.
        series_fields: Fields to read from the series.
        left_axis_fields: Fields to associate with the left axis.
        right_axis_fields: Fields to associate with the left axis.

    Returns:
        Series data as a dictionary.
    """
    if len(series_fields) < 1:
        series_fields = ["/"]  # special field to expand all
    if index is not None and index not in series_fields:
        series_fields.append(index)
    series: Dict[str, list] = {field: [] for field in series_fields}
    found_once = {field: False for field in series_fields}
    if index is None:
        series["__index__"] = []
        found_once["__index__"] = True
    unpacked_index = 0
    for unpacked in decode_json(file=file):
        expand_fields = []
        for field in series_fields:
            try:
                keys = field.split("/")
                if len(keys[0]) < 1:
                    raise FieldNeedsExpansion(list(unpacked.keys()))
                value = get_from_keys(unpacked, keys)
                found_once[field] = True
            except KeyError as key_error:
                value = "null"
                if field == index:
                    raise ValueError(
                        f'Index "{field}" undefined '
                        f"in unpacked item number {unpacked_index}"
                    ) from key_error
            except FieldNeedsExpansion as exn:
                value = "null"
                if len(exn.subfields) > 0:  # o/w wait for non-empty
                    expand_fields.append((field, exn.subfields))
            series[field].append(value)
        if index is None:
            series["__index__"].append(unpacked_index)
            unpacked_index += 1
        for (old_field, subfields) in expand_fields:
            series_fields.remove(old_field)
            values_so_far = series[old_field]
            axis_list = (
                left_axis_fields
                if old_field in left_axis_fields
                else right_axis_fields
            )
            axis_list.remove(old_field)
            del series[old_field]
            del found_once[old_field]
            for subfield in subfields:
                new_field = f"{old_field}/{subfield}"
                series_fields.append(new_field)
                series[new_field] = list(values_so_far)
                found_once[new_field] = False
                axis_list.append(new_field)
        if len(series_fields) > len(ColorPicker.COLORS):
            series_fields.remove("time")
            raise ValueError(
                "Too many fields (not enough colors!): "
                " ".join(series_fields)
            )
    for field in series_fields:
        if not found_once[field]:
            logging.warning("Field %s not found", field)

    html = generate_html(
        args.title,
        series,
        left_axis_fields,
        right_axis_fields,
        args.left_axis_unit,
        args.right_axis_unit,
    )

    with tempfile.NamedTemporaryFile(
        mode="w+",
        prefix=f"plot-{datetime.now().strftime('%Y%m%d-%H%M%S')}-",
        suffix=".html",
        delete=False,
    ) as output_file:
        output_file.write(html)
        webbrowser.open_new_tab(output_file.name)
