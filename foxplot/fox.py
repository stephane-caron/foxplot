#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

"""Main class to manipulate dictionary-series data."""

import logging
import sys
import webbrowser
from typing import BinaryIO, List, Optional, TextIO, Union

from .decoders.json import decode_json
from .decoders.msgpack import decode_msgpack
from .generate_html import generate_html
from .node import Node
from .series import Series
from .write_tmpfile import write_tmpfile


class Fox:
    """Frequent Observation diXionaries, our main class.

    Our main class to read, access and manipulate series of dictionary data.
    """

    __file: Optional[str]
    __time: Optional[str]
    data: Node
    length: int

    def __init__(
        self,
        from_file: Optional[str] = None,
        time: Union[None, str, Series] = None,
    ):
        """Initialize series.

        Args:
            from_file: If set, read data from this path.
            time: Label of time index in input dictionaries.
        """
        self.__file = from_file
        self.__time = None
        self.data = Node("/")
        self.length = 0
        if from_file:
            self.read_from_file(from_file)
        if time is not None:
            self.set_time(time)

    def get_series(self, label: str) -> Series:
        """Get time-series data from a given label.

        Args:
            label: Label to the data in input dictionaries, for example
                ``/observation/cpu_temperature``.

        Returns:
            Corresponding time series.
        """
        keys = label.strip("/").split("/")
        return self.data._get_child(keys)

    @property
    def labels(self) -> List[str]:
        """List of all labels present in the data."""
        return self.data._list_labels()

    def __print_command_line(self, left_series, right_series):
        print("The command line to generate this plot is:\n")
        left_args = " ".join(left_series.keys())
        right_args = (
            f"-r {' '.join(right_series.keys())} " if right_series else ""
        )
        file = self.__file if self.__file is not None else ""
        timestamp = f"-t {self.__time} " if self.__time is not None else ""
        print(f"foxplot {timestamp}-l {left_args} {right_args}{file}")

    def plot(
        self,
        left: Union[Series, Node, List[Union[Series, Node]]],
        right: Optional[List[Series]] = None,
        title: Optional[str] = None,
        left_axis_unit: str = "",
        right_axis_unit: str = "",
        print_command_line: bool = False,
    ) -> None:
        """Plot a set of indexed series.

        Args:
            left: Series to plot on the left axis.
            right: Series to plot on the right axis.
            title: Plot title.
            left_axis_unit: Unit label for the left axis.
            right_axis_unit: Unit label for the right axis.
            print_command_line: If true, print out how to obtain the plot from
                the command line.
        """
        if isinstance(left, Series) or isinstance(left, Node):
            left = [left]
        if title is None:
            title = f"Plot from {self.__file}"

        times = (
            self.get_series(self.__time)._get(self.length)
            if self.__time is not None
            else [float(x) for x in range(self.length)]
        )

        def list_to_dict(series_list):
            series_dict = {}
            for series in series_list:
                if isinstance(series, Series):
                    series_dict[series._label] = series._get(self.length)
                elif isinstance(series, Node):
                    for key, child in series._items():
                        label = series._label + f"/{key}"
                        if isinstance(child, Series):
                            series_dict[label] = child._get(self.length)
                        else:
                            logging.warn(
                                "Skipping '%s' as it is not an indexed series",
                                label,
                            )
                else:
                    raise TypeError(
                        f"Series '{series._label}' "
                        f"has unknown type {type(series)}"
                    )
            return series_dict

        left_series = list_to_dict(left)
        right_series = list_to_dict(right) if right is not None else {}
        html = generate_html(
            times,
            left_series,
            right_series,
            title,
            left_axis_unit,
            right_axis_unit,
            timestamped=self.__time is not None,
        )

        filename = write_tmpfile(html)
        webbrowser.open_new_tab(filename)
        if print_command_line:
            self.__print_command_line(left_series, right_series)

    def read_from_file(self, filename: str) -> None:
        """Process time series data.

        Args:
            filename: Name of a file to read time series from.
        """
        if filename == "stdin":
            self.read_from_json(sys.stdin)
        elif filename.endswith(".json"):
            with open(filename, "r", encoding="utf-8") as file:
                self.read_from_json(file)
        elif filename.endswith(".mpack"):
            with open(filename, "rb") as file:
                self.read_from_msgpack(file)

    def read_from_json(self, file: TextIO) -> None:
        """Process time series data from a JSON stream.

        Args:
            file: JSON stream to read time series from.
        """
        for unpacked in decode_json(file=file):
            self.unpack(unpacked)

    def read_from_msgpack(self, file: BinaryIO) -> None:
        """Process time series data from a MessagePack stream.

        Args:
            file: MessagePack stream to read time series from.
        """
        for unpacked in decode_msgpack(file=file):
            self.unpack(unpacked)

    def set_time(self, time: Union[str, Series]):
        """Set label of time index in input dictionaries.

        Args:
            time: Time index as a series or its label in input dictionaries.
        """
        label = time._label if isinstance(time, Series) else time
        self.__time = label

    def unpack(self, unpacked: dict) -> None:
        """Append data from an unpacked dictionary.

        Args:
            unpacked: Unpacked dictionary.
        """
        self.data._update(self.length, unpacked)
        self.length += 1

    def detect_time(self) -> None:
        """Search for a time key in root keys."""
        candidates = ("time", "timestamp")
        for key in candidates:
            if key in self.data.__dict__:
                self.set_time(self.data.__dict__[key])
                print(
                    f'Detected "{key}" as time key from the input '
                    "(call `fox.set_time` to select a different one)"
                )
                return
