#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Series data unpacked from input dictionaries."""

from os.path import commonprefix

from numpy.typing import NDArray

from .series import Series


def _operator_label(op: str, label: str, other_label: str) -> str:
    prefix = commonprefix([label, other_label])
    n = len(prefix)
    return f"{prefix}({label[n:]} {op} {other_label[n:]})"


class FrozenSeries(Series):
    """Time-series values."""

    _values: NDArray[float]

    def __init__(self, label: str, values: NDArray[float]):
        """Initialize a new series.

        Args:
            label: Label of the series in the input data.
            values: Values as a NumPy array.
        """
        super().__init__(label)
        self._values = values

    def __len__(self):
        """Length of the indexed series."""
        return self._values.shape[0]

    def __repr__(self):
        """String representation of the series."""
        return f"Time series with values: {self._values}"

    def __add__(self, other):
        """Sum of two series.

        Args:
            other: Other series.
        """
        sum_label = _operator_label("+", self._label, other._label)
        return FrozenSeries(sum_label, self._values + other._values)

    def __mul__(self, other):
        """Product between two series.

        Args:
            other: Other series.
        """
        product_label = _operator_label("*", self._label, other._label)
        return FrozenSeries(product_label, self._values * other._values)
