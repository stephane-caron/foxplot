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
from datetime import datetime
from os import path
from typing import List

from .plot import plot
from .series import NestedDict


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
        "--interactive",
        action="store_true",
        default=False,
        help="interact with the data from a Python interpreter",
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
        help="key to use as time index for the series",
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


def main() -> None:
    """Entry point for command-line execution."""
    args = parse_command_line_arguments()

    fox = NestedDict()
    if args.file is not None:
        with open(args.file, "r", encoding="utf-8") as file:
            max_index = fox.read_from_file(file)
    else:  # args.file is None:
        max_index = fox.read_from_file(sys.stdin)

    times = fox.get_series(args.time, max_index)
    if args.interactive:
        __import__("IPython").embed()
    else:  # not args.interactive
        left_axis_fields = args.left if args.left else []
        right_axis_fields = args.right if args.right else []
        plot(
            times,
            fox,
            max_index,
            left_axis_fields,
            right_axis_fields,
            args.title,
            args.left_axis_unit,
            args.right_axis_unit,
        )
