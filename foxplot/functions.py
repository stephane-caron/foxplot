#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Functions that can be applied to frozen series."""

import numpy as np

from .frozen_series import FrozenSeries


def abs(series: FrozenSeries) -> FrozenSeries:
    """Return the series of absolute values of another series.

    Args:
        series: Series to compute absolute values from.

    Returns:
        Array of windowed standard deviations along the series.
    """
    label = f"abs({series._label})"
    values = np.abs(series._values)
    return FrozenSeries(label, values)


def estimate_lag(
    time: FrozenSeries,
    input: FrozenSeries,
    output: FrozenSeries,
) -> FrozenSeries:
    """Estimate input-output response as a first-order low-pass filter.

    Args:
        time: Times corresponding to inputs and outputs.
        input: Input values.
        output: Output values.

    Returns:
        Array of lag estimates, where the lag is defined as the cutoff period
        of the estimated first-order low-pass filter.

    We carry out the cutoff period of a corresponding low-pass filter by online
    simplie linear regression, as described for instance in this note:
    https://scaron.info/blog/simple-linear-regression-with-online-updates.html
    """
    label = f"lag(input={input._label}, output={output._label})"
    dot_uu = 0.0
    dot_uv = 0.0
    nb_steps = len(time)
    values = [np.nan]
    for i in range(nb_steps - 1):
        dt = time._values[i + 1] - time._values[i]
        u = input._values[i] - output._values[i]
        v = output._values[i + 1] - output._values[i]
        if np.isnan(dt) or np.isnan(u) or np.isnan(v):
            values.append(np.nan)
            continue
        dot_uu += u * u
        dot_uv += u * v
        if dot_uu < 1e-10:
            values.append(np.nan)
            continue
        exp_lag_dt = dot_uv / dot_uu
        if exp_lag_dt < 1e-10:
            values.append(np.nan)
            continue
        lag = np.log(exp_lag_dt) / dt
        values.append(lag)
    return FrozenSeries(label, np.array(values))


def std(series: FrozenSeries, window_size: int) -> FrozenSeries:
    """Return the rolling standard deviation of the series.

    Args:
        series: Series to compute standard deviations from.
        window_size: Size of the rolling window in which to compute
            standard deviations.

    Returns:
        Array of windowed standard deviations along the series.
    """
    label = f"std({series._label}, {window_size})"
    values = np.std(
        np.lib.stride_tricks.sliding_window_view(series._values, window_size),
        axis=-1,
    )
    return FrozenSeries(label, values)
