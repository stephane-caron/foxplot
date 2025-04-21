#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Series data unpacked from input dictionaries."""

import logging
from os.path import commonprefix
from typing import Dict, Literal, Optional

import numpy as np
from numpy.typing import NDArray

from .labeled_series import LabeledSeries

UNIT_TO_SECONDS: Dict[str, float] = {
    "s": 1.0,
    "M": 60.0,
    "H": 3600.0,
    "d": 3600.0 * 24.0,
    "m": 3600.0 * 24.0 * 30.0,
    "y": 3600.0 * 24.0 * 365.0,
}


def _operator_label(op: str, label: str, other_label: str) -> str:
    prefix = commonprefix([label, other_label])
    n = len(prefix)
    return f"{prefix}({label[n:]} {op} {other_label[n:]})"


class Series(LabeledSeries):
    """Front class for time-series that users interact with."""

    _times: Optional[NDArray[np.float64]]
    _values: NDArray[np.float64]

    def __init__(
        self,
        label: str,
        values: NDArray[np.float64],
        times: Optional[NDArray[np.float64]],
    ):
        """Initialize a new series.

        Args:
            label: Label of the series in the input data.
            values: Values as a NumPy array.
            times: Corresponding time values as a NumPy array.
        """
        super().__init__(label)
        self._times = times
        self._values = values

    def __add__(self, other) -> "Series":
        """Sum of two series.

        Args:
            other: Other series.
        """
        return Series(
            label=_operator_label("+", self._label, other._label),
            values=self._values + other._values,
            times=self._times,
        )

    def __len__(self) -> int:
        """Length of the indexed series."""
        return self._values.shape[0]

    def __mul__(self, other) -> "Series":
        """Elementwise product between two series.

        Args:
            other: Other series.
        """
        if np.isscalar(other):
            return Series(
                label=_operator_label("*", self._label, str(other)),
                values=self._values * other,
                times=self._times,
            )
        return Series(
            label=_operator_label("*", self._label, other._label),
            values=self._values * other._values,
            times=self._times,
        )

    def __neg__(self) -> "Series":
        """Unitary minus applied to the series."""
        return Series(
            label=f"-{self._label}",
            values=-self._values,
            times=self._times,
        )

    def __repr__(self) -> str:
        """String representation of the series."""
        return f"Time series with values: {self._values}"

    def __truediv__(self, other) -> "Series":
        """Elementwise ratio between two series.

        Args:
            other: Other series.
        """
        if np.isscalar(other):
            return Series(
                label=_operator_label("/", self._label, str(other)),
                values=self._values / other,
                times=self._times,
            )
        return Series(
            label=_operator_label("/", self._label, other._label),
            values=self._values / other._values,
            times=self._times,
        )

    def abs(self) -> "Series":
        """Return the series of absolute values of this series.

        Returns:
            Array of windowed standard deviations along the series.
        """
        return Series(
            label=f"abs({self._label})",
            values=np.abs(self._values),
            times=self._times,
        )

    def deriv(
        self,
        unit: Literal["s", "M", "H", "d", "m", "y"],
        cutoff: float = 0.0,
    ) -> "Series":
        """Time-derivative with optional low-pass filtering.

        Args:
            unit: String specifying the time unit of the time derivative, and
                of the time constant, if provided. Use "s" for seconds
                (default), "M" for minute, "H" for hour, "d" for day, "m" for
                month and "y" for year.
            cutoff: Cutoff period of low-pass filtering, in seconds.

        Returns:
            Finite-difference derivative of the time series. If the series has
            unit [U], its time-derivative will be in [U] / [T] where [T] is the
            time unit specified by ``unit`` (default: second).
        """
        nb_steps = len(self._times)
        filtered_output = None
        outputs = []
        cutoff_period_s = UNIT_TO_SECONDS[unit] * cutoff
        for i in range(nb_steps - 1):
            dt = self._times[i + 1] - self._times[i]
            if dt < 0.0:
                logging.warning(
                    "Invalid timestep dt=%f at time=%f",
                    dt,
                    self._times[i],
                )
                outputs.append(np.nan)
                continue
            finite_diff = (self._values[i + 1] - self._values[i]) / dt
            if cutoff_period_s < 2 * dt or filtered_output is None:
                # Nyquist-Shannon sampling theorem (again)
                filtered_output = finite_diff
                outputs.append(finite_diff)
            else:  # low-pass filtering
                gamma = 1.0 - np.exp(-dt / cutoff_period_s)
                filtered_output += gamma * (finite_diff - filtered_output)
                outputs.append(filtered_output)
        outputs.append(outputs[-1])
        assert len(outputs) == len(self._values) == len(self._times)
        label = f"deriv({self._label}, unit={unit}"
        if cutoff > 1e-10:
            label += f", cutoff={cutoff} {unit}"
        label += ")"
        return Series(
            label=label,
            values=np.array(outputs) * UNIT_TO_SECONDS[unit],
            times=self._times,
        )

    def low_pass_filter(self, T: float) -> "Series":
        """Apply low-pass filter to a time series.

        Args:
            T: Cutoff period of the low-pass filter.

        Returns:
            Low-pass filtered time series.
        """
        nb_steps = len(self._times)
        output = self._values[0]
        outputs = [output]
        for i in range(nb_steps - 1):
            dt = self._times[i + 1] - self._times[i]
            if T < 2 * dt:
                logging.warning(
                    "Nyquist-Shannon sampling theorem: "
                    "at time=%f, dt=%f but T=%f",
                    self._times[i],
                    dt,
                    T,
                )
                outputs.append(np.nan)
                continue
            forgetting_factor = np.exp(-dt / T)
            output += (1.0 - forgetting_factor) * (self._values[i] - output)
            outputs.append(output)
        assert len(outputs) == len(self._values) == len(self._times)
        return Series(
            label=f"low_pass_filter({self._label}, {T=})",
            values=np.array(outputs),
            times=self._times,
        )

    def std(self, window_size: int) -> "Series":
        """Return the rolling standard deviation of the series.

        Args:
            window_size: Size of the rolling window in which to compute
                standard deviations.

        Returns:
            Array of windowed standard deviations along the series.
        """
        return Series(
            label=f"std({self._label}, {window_size})",
            values=np.std(
                np.lib.stride_tricks.sliding_window_view(
                    self._values, window_size
                ),
                axis=-1,
            ),
            times=self._times,
        )
