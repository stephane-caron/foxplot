#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Series data unpacked from input dictionaries."""

from typing import Any, Dict

import numpy as np

from .frozen_series import FrozenSeries
from .series import Series


class HotSeries(Series):
    """Indexed time-series in which we are still inserting values.

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

    def _freeze(self, max_index: int) -> FrozenSeries:
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
        return FrozenSeries(self._label, np.array(values, dtype=np.float64))
