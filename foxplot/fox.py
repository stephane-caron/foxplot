#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""Main class to manipulate dictionary-series data."""

import logging
import sys
import webbrowser
from typing import BinaryIO, Dict, List, Optional, TextIO, Union

import numpy as np
from numpy.typing import NDArray

from .decoders.json import decode_json
from .decoders.msgpack import decode_msgpack
from .frozen_series import FrozenSeries
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

    def get_frozen_series(self, label: str) -> FrozenSeries:
        """Get time-series data from a given label.

        Args:
            label: Label to the data in input dictionaries, for example
                ``/observation/cpu_temperature``.

        Returns:
            Corresponding time series.
        """
        keys = label.strip("/").split("/")
        series = self.data._get_child(keys)
        if not isinstance(series, FrozenSeries):
            raise TypeError(f"Series {label} is not frozen")
        return series

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

    def __list_to_dict(
        self, series_list: List[Union[Series, Node]]
    ) -> Dict[str, NDArray[np.float64]]:
        """Convert a list of series (or nodes) to a dictionary.

        The output dictionary has one key per series in the list. Nodes are
        expanded just once, assuming all their children in the data tree
        are series.

        Args:
            series_list: Input list of series;

        Returns:
            Dictionary mapping series names to their values.
        """
        series_dict = {}
        for series in series_list:
            if isinstance(series, FrozenSeries):
                series_dict[series._label] = series._values
            elif isinstance(series, Node):
                for key, child in series._items():
                    label = series._label + f"/{key}"
                    if isinstance(child, FrozenSeries):
                        series_dict[label] = child._values
                    else:
                        logging.warn(
                            "Skipping '%s' as it is not an indexed series",
                            label,
                        )
            else:
                raise TypeError(
                    f"Series '{series}' has unhandled type {type(series)}"
                )
        return series_dict

    def plot(
        self,
        left: Union[Series, Node, List[Union[Series, Node]]],
        right: Optional[Union[Series, Node, List[Union[Series, Node]]]] = None,
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
        if isinstance(right, Series) or isinstance(right, Node):
            right = [right]
        if title is None:
            title = f"Plot from {self.__file}"

        times: NDArray[np.float64] = (
            self.get_frozen_series(self.__time)._values
            if self.__time is not None
            else np.array(range(self.length), dtype=np.float64)
        )

        left_series: Dict[str, NDArray[np.float64]] = self.__list_to_dict(left)
        right_series: Dict[str, NDArray[np.float64]] = {}
        if right is not None:
            right_series = self.__list_to_dict(right)
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
        self.data._freeze(self.length)

    def read_from_msgpack(self, file: BinaryIO) -> None:
        """Process time series data from a MessagePack stream.

        Args:
            file: MessagePack stream to read time series from.
        """
        for unpacked in decode_msgpack(file=file):
            self.unpack(unpacked)
        self.data._freeze(self.length)

    def unpack(self, unpacked: dict) -> None:
        """Append data from an unpacked dictionary.

        Args:
            unpacked: Unpacked dictionary.
        """
        self.data._update(self.length, unpacked)
        self.length += 1

    def freeze(self):
        """Freeze all time series at the current input length."""
        self.data._freeze(self.length)

    def set_time(self, time: Union[str, Series]):
        """Set label of time index in input dictionaries.

        Args:
            time: Time index as a series or its label in input dictionaries.
        """
        label = time._label if isinstance(time, Series) else time
        self.__time = label

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
