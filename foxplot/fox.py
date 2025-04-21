#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""The :class:`Fox` class is where we manipulate dictionary-series data."""

import logging
from pathlib import PosixPath
from typing import Dict, List, Optional, Union

import numpy as np
import uplot
from numpy.typing import NDArray

from .decode import decode
from .node import Node
from .series import Series


class Fox:
    """Frequent Observation diXionaries, our main class.

    Our main class to read, access and manipulate series of dictionary data.
    """

    __source: Union[str, PosixPath]
    __time_label: Optional[str]
    data: Node
    length: int

    @staticmethod
    def empty() -> "Fox":
        """Initialize from empty time series."""
        return Fox(filename=None)

    def __init__(self, filename: Union[str, PosixPath, None]) -> None:
        """Initialize time series.

        Args:
            filename: Name (e.g. "stdin") or path of file to read time series
                from, or ``None`` to start from an empty state.
        """
        self.__source = filename or "custom data"
        self.__time_label = None
        self.data = Node("/")
        self.length = 0
        if filename is not None:
            for unpacked in decode(filename):
                self.unpack(unpacked)
            self.data._freeze(self.length)

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
            if isinstance(series, Series):
                series_dict[series._label] = series._values
            elif isinstance(series, Node):
                for key, child in series._items():
                    label = series._label + f"/{key}"
                    if isinstance(child, Series):
                        series_dict[label] = child._values
                    else:
                        logging.warning(
                            "Skipping '%s' as it is not an indexed series",
                            label,
                        )
            else:
                raise TypeError(
                    f"Series '{series}' has unhandled type {type(series)}"
                )
        return series_dict

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

    def get_series(self, label: str) -> Series:
        """Get time-series data from a given label.

        Args:
            label: Label to the data in input dictionaries, for example
                ``/observation/cpu_temperature``.

        Returns:
            Corresponding time series.
        """
        keys = label.strip("/").split("/")
        series = self.data._get_child(keys)
        if not isinstance(series, Series):
            raise TypeError(f"Series {label} is not finalized")
        return series

    def plot(
        self,
        left: Union[Series, Node, List[Union[Series, Node]]],
        right: Optional[Union[Series, Node, List[Union[Series, Node]]]] = None,
        title: Optional[str] = None,
    ) -> None:
        """Plot a set of indexed series.

        Args:
            left: Series to plot on the left axis.
            right: Series to plot on the right axis.
            title: Plot title.
        """
        if isinstance(left, (Node, Series)):
            left = [left]
        if isinstance(right, (Node, Series)):
            right = [right]
        if title is None:
            title = f"Plot from {self.__source}"

        times: NDArray[np.float64] = (
            self.get_frozen_series(self.__time_label)._values
            if self.__time_label is not None
            else np.array(range(self.length), dtype=np.float64)
        )

        left_series: Dict[str, NDArray[np.float64]] = self.__list_to_dict(left)
        right_series: Dict[str, NDArray[np.float64]] = {}
        if right is not None:
            right_series = self.__list_to_dict(right)
        uplot.plot2(
            times,
            list(left_series.values()),
            list(right_series.values()),
            title=title,
            timestamped=self.__time_label is not None,
            left_labels=list(left_series.keys()),
            right_labels=list(right_series.keys()),
        )

    def unpack(self, unpacked: dict) -> None:
        """Append data from an unpacked dictionary.

        Args:
            unpacked: Unpacked dictionary.
        """
        self.data._update(self.length, unpacked)
        self.length += 1

    def set_time(self, time: Series):
        """Set label of time index in input dictionaries.

        Args:
            time: Time index as a series.
        """
        time._values = time._values.astype(np.float64)
        label = time._label if isinstance(time, Series) else time
        self.__time_label = label

        def set_series_times(series: Union[Series, Node]):
            if isinstance(series, Series):
                series._times = self.__times
            if isinstance(series, Node):
                for key, child in series._items():
                    set_series_times(child)

        set_series_times(self.data)
