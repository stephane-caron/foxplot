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
