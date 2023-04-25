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

"""Main class to manipulate dictionary-series data."""

import webbrowser
from typing import List, Optional, TextIO

from .decoders.json import decode_json
from .generate_html import generate_html
from .series import SeriesValue
from .node import Node
from .write_tmpfile import write_tmpfile


class Fox:
    """Frequent Observation diXionaries, our main class.

    Our main class to read, access and manipulate series of dictionary data.
    """

    __time: str
    data: Node
    length: int

    def __init__(self, time: str):
        """Initialize series.

        Args:
            time: Label of time index in input dictionaries.
        """
        self.__time = time
        self.data = Node("/")
        self.length = 0

    def get_series(self, label: str) -> SeriesValue:
        """
        Get time-series data from a given label.

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

    def read_from_file(self, file: TextIO) -> None:
        """Process time series data.

        Args:
            file: File to read time series from.
        """
        for unpacked in decode_json(file=file):
            self.unpack(unpacked)

    def unpack(self, unpacked: dict) -> None:
        self.data._update(self.length, unpacked)
        self.length += 1

    def plot(
        self,
        left: List[SeriesValue],
        right: Optional[List[SeriesValue]] = None,
        title: str = "",
        left_axis_unit: str = "",
        right_axis_unit: str = "",
        open: bool = True,
    ) -> None:
        times = (
            self.get_series(self.__time)._get(self.length)
            if self.__time is not None
            else [float(x) for x in range(self.length)]
        )
        left_series = {
            series.label: series._get(self.length) for series in left
        }
        right_series = {
            series.label: series._get(self.length)
            for series in (right if right is not None else [])
        }
        html = generate_html(
            times,
            left_series,
            right_series,
            title,
            left_axis_unit,
            right_axis_unit,
            timestamped=self.__time is not None,
        )
        if open:
            filename = write_tmpfile(html)
            webbrowser.open_new_tab(filename)
        else:  # print command line
            left_args = "-l ".join(left_series.keys())
            right_args = ("-r " if right_series else "") + "-r ".join(
                right_series.keys()
            )
            print(f"foxplot -t {self.__time} -l {left_args} {right_args}")
