#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""The :class:`Fox` class is where we manipulate dictionary-series data."""

import logging
from typing import Dict, List, Optional, Union

import numpy as np
import uplot
from numpy.typing import NDArray

from .decode import decode
from .frozen_series import FrozenSeries
from .node import Node
from .series import Series


class Fox:
    """Frequent Observation diXionaries, our main class.

    Our main class to read, access and manipulate series of dictionary data.
    """

    __filename: Optional[str]
    __time_label: Optional[str]
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
        self.__filename = from_file
        self.__time_label = None
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
                        logging.warning(
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
    ) -> None:
        """Plot a set of indexed series.

        Args:
            left: Series to plot on the left axis.
            right: Series to plot on the right axis.
            title: Plot title.
            left_axis_unit: Unit label for the left axis.
            right_axis_unit: Unit label for the right axis.
        """
        if isinstance(left, Series) or isinstance(left, Node):
            left = [left]
        if isinstance(right, Series) or isinstance(right, Node):
            right = [right]
        if title is None:
            title = f"Plot from {self.__filename}"

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
            time=self.__time_label is not None,
            left_labels=list(left_series.keys()),
            right_labels=list(right_series.keys()),
        )

    def read_from_file(self, filename: str) -> None:
        """Process time series data.

        Args:
            filename: Name of a file to read time series from.
        """
        for unpacked in decode(filename):
            self.unpack(unpacked)
        self.data._freeze(self.length)

    def unpack(self, unpacked: dict) -> None:
        """Append data from an unpacked dictionary.

        Args:
            unpacked: Unpacked dictionary.
        """
        self.data._update(self.length, unpacked)
        self.length += 1

    def set_time(self, time: Union[str, Series]):
        """Set label of time index in input dictionaries.

        Args:
            time: Time index as a series or its label in input dictionaries.
        """
        time._values = time._values.astype(np.float64)
        label = time._label if isinstance(time, Series) else time
        self.__time_label = label

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
