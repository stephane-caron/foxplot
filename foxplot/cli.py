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

from .fox import Fox


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
        help="series to plot using the (default) left axis",
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
        help="series to plot using the right axis",
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


def main() -> None:
    """Entry point for command-line execution."""
    args = parse_command_line_arguments()

    fox = Fox(from_file=args.file, time=args.time)
    if args.file is None:
        fox.read_from_json(sys.stdin)

    nothing_to_plot = not args.left and not args.right
    if args.interactive or nothing_to_plot:
        usage = (
            "-" * 68 + "\n\n\n"
            "Welcome to foxplot!\n\n"
            "Explore your time series in ``data`` (tab completion works).\n"
            "When you know what you want, plot time series with:\n\n"
            "    fox.plot(\n"
            "        left=[data.foo.bar, data.other.bar],\n"
            "        right=[data.something.else],\n"
            "        time=data.timestamp,\n"
            '        title="My awesome plot",\n'
            "    )"
        )
        __import__("IPython").embed(
            header=usage,
            user_ns={
                "data": fox.data,
                "fox": fox,
            },
        )
    else:  # not args.interactive
        left_labels = args.left if args.left else []
        right_labels = args.right if args.right else []
        left_series = [fox.get_series(label) for label in left_labels]
        right_series = [fox.get_series(label) for label in right_labels]
        fox.plot(
            left_series,
            right_series,
            args.title,
            args.left_axis_unit,
            args.right_axis_unit,
        )
