#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Functions that can be applied to frozen series."""

import numpy as np

from .frozen_series import FrozenSeries
from .node import Node


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
    time_constant: float,
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
    nb_steps = len(time)
    slopes = [np.nan]
    intercepts = [np.nan]
    lags = [np.nan]
    dots = np.zeros(5)
    for i in range(nb_steps - 1):
        dt = time._values[i + 1] - time._values[i]
        x = input._values[i] - output._values[i]
        y = output._values[i + 1] - output._values[i]
        if np.isnan(dt) or np.isnan(x) or np.isnan(y):
            slopes.append(np.nan)
            intercepts.append(np.nan)
            lags.append(np.nan)
            continue
        forgetting_factor = np.exp(-dt / time_constant)
        dots *= forgetting_factor
        dots += np.array([1.0, x, y, x * x, x * y])
        dot_11, dot_1x, dot_1y, dot_xx, dot_xy = dots
        det = dot_11 * dot_xx - dot_1x**2
        if det < 1e-10:
            slopes.append(np.nan)
            intercepts.append(np.nan)
            lags.append(np.nan)
            continue
        intercept = (dot_xx * dot_1y - dot_xy * dot_1x) / det
        slope = (dot_xy * dot_11 - dot_1x * dot_1y) / det
        if slope < 1e-10:
            slopes.append(np.nan)
            intercepts.append(np.nan)
            lags.append(np.nan)
            continue
        # slope = exp(-dt / lag)
        lag = -dt / np.log(slope)
        intercepts.append(intercept)
        slopes.append(slope)
        lags.append(lag)
    node = Node(label)
    children = {
        "slope": np.array(slopes),
        "intercept": np.array(intercepts),
        "lag": np.array(lags),
    }
    node.__dict__.update(
        {
            key: FrozenSeries(f"{label}/{key}", value)
            for key, value in children.items()
        }
    )
    return node


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
