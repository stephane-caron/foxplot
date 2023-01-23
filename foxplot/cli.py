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
        fields.extend(f"{key}/{field}" for field in get_fields(data[key]))
    return fields


def get_from_keys(collection: Union[dict, list], keys: List[Union[int, str]]):
    """
    Get value `collection[key1][key2][...][keyN]` from a nested dictionary
    `collection` and keys `[key1, key2, ..., keyN]`.

    Args:
        collection: Dictionary or list to get value from.
        keys: Sequence of keys to the value.
    """
    key = keys[0]
    if isinstance(collection, list):
        key = int(key)
    if len(keys) > 1:
        return get_from_keys(collection[key], keys[1:])
    value = collection[key]
    if isinstance(value, dict):
        raise FieldNeedsExpansion(value.keys())
    if isinstance(value, list):
        raise FieldNeedsExpansion(range(len(value)))
    return value


def main() -> None:
    """
    Entry point for command-line execution.
    """
    args = parse_command_line_arguments()
    series_fields = [] if "time" in args.field else ["time"]
    left_axis_fields = []
    right_axis_fields = []
    for field in args.field:
        if field.startswith("R:"):
            field = field[2:]
            right_axis_fields.append(field)
        else:  # left-axis field
            left_axis_fields.append(field)
        series_fields.append(field)
    series: Dict[str, list] = {field: [] for field in series_fields}
    found_once = {field: False for field in series_fields}
    for unpacked in decode_json(file=sys.stdin):
        expand_fields = []
        for field in series_fields:
            try:
                keys = field.split("/")
                value = get_from_keys(unpacked, keys)
                found_once[field] = True
            except KeyError:
                value = "null"
            except FieldNeedsExpansion as exn:
                value = "null"
                if len(exn.subfields) > 0:  # o/w wait for non-empty
                    expand_fields.append((field, exn.subfields))
            series[field].append(value)
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
