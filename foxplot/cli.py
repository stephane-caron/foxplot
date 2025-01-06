#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Command-line entry point for foxplot."""

import argparse
import sys
from datetime import datetime
from typing import List, Union

from .fox import Fox
from .functions import abs as abs_func
from .functions import deriv as deriv_func
from .functions import estimate_lag as estimate_lag_func
from .functions import low_pass_filter as low_pass_filter_func
from .functions import std as std_func
from .node import Node
from .series import Series


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


def get_function_description(f):
    """Get the short description of a function as a string."""
    return f.__doc__.split("\n")[0]


def main() -> None:
    """Entry point for command-line execution."""
    args = parse_command_line_arguments()

    fox = Fox(from_file=args.file, time=args.time)
    if args.file is None:
        fox.read_from_json(sys.stdin)
    fox.detect_time()

    nothing_to_plot = not args.left and not args.right
    user_ns = {
        "data": fox.data,
        "fox": fox,
    }
    functions = {
        "abs": abs_func,
        "deriv": deriv_func,
        "estimate_lag": estimate_lag_func,
        "low_pass_filter": low_pass_filter_func,
        "std": std_func,
    }
    user_ns.update(functions)
    if args.interactive or nothing_to_plot:
        usage = (
            "Welcome to foxplot!\n"
            "\n"
            "Explore your time series in `data` (tab completion works).\n"
            "When you know what you want, plot your time series with:\n"
            "\n"
            "    fox.plot(\n"
            "        left=[data.foo.bar, data.other.bar],\n"
            "        right=[data.something.else],\n"
            '        title="My awesome plot",\n'
            "    )\n"
            "\n"
            "You can also apply the following functions to time series:\n"
            "\n"
            + "\n".join(
                f"- `{key}`: {get_function_description(func)}"
                for key, func in functions.items()
            )
        )
        __import__("IPython").embed(
            header=usage,
            user_ns={
                "abs": abs_func,
                "data": fox.data,
                "deriv": deriv_func,
                "estimate_lag": estimate_lag_func,
                "fox": fox,
                "low_pass_filter": low_pass_filter_func,
                "std": std_func,
            },
        )
    else:  # not args.interactive
        left_labels = args.left if args.left else []
        right_labels = args.right if args.right else []
        left_series: List[Union[Series, Node]] = [
            fox.get_frozen_series(label) for label in left_labels
        ]
        right_series: List[Union[Series, Node]] = [
            fox.get_frozen_series(label) for label in right_labels
        ]
        fox.plot(
            left_series,
            right_series,
            args.title,
            args.left_axis_unit,
            args.right_axis_unit,
        )
