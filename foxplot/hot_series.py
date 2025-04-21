#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Series data unpacked from input dictionaries."""

from typing import Any, Dict

import numpy as np

from .labeled_series import LabeledSeries
from .series import Series


class HotSeries(LabeledSeries):
    """Indexed time-series in which we can still insert values.

    Internally, this datastructure maps time indexes (the corresponding times
    themselves are stored in a different list) to values.
    """

    __indexed_values: Dict[int, Any]

    def __init__(self, label: str):
        """Initialize a new indexed series.

        Args:
            label: Label of the series in the input data.
        """
        super().__init__(label)
        self.__indexed_values = {}

    def __len__(self):
        """Length of the indexed series."""
        return len(self.__indexed_values)

    def __repr__(self):
        """String representation of the series."""
        values = list(self.__indexed_values.values())
        return f"Time series with values: {values}"

    def _update(self, index: int, value: Any) -> None:
        """Update the value at a given time index.

        Args:
            index: Time index.
            value: New value.
        """
        self.__indexed_values[index] = value

    def _freeze(self, max_index: int) -> Series:
        """Get indexed series as a list of values.

        Args:
            max_index: The output list will range from 0 (first time from the
                input) to this maximum index (excluded).

        Returns:
            Indexed series as a list of values.
        """
        last_value = None
        values = []
        for index in range(max_index):
            last_value = self.__indexed_values.get(index, last_value)
            values.append(last_value)
        array = (
            np.array(values, dtype=np.float64)
            if isinstance(last_value, (int, float))
            else np.array(values)
        )
        return Series(label=self._label, values=array, times=None)
