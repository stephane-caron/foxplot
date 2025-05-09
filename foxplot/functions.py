#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Functions that can be applied to series."""

import logging

import numpy as np

from .node import Node
from .series import Series


def estimate_lag(
    time: Series,
    input: Series,
    output: Series,
    time_constant: float,
) -> Node:
    """Estimate input-output response as a first-order low-pass filter.

    Args:
        time: Times corresponding to inputs and outputs.
        input: Input values.
        output: Output values.
        time_constant: Time-constant of the estimation's sliding window.

    Returns:
        Array of lag estimates, where the lag is defined as the cutoff period
        of the estimated first-order low-pass filter.

    We carry out the cutoff period of a corresponding low-pass filter by
    sliding-window online linear regression, as described .e.g in `this note
    <https://scaron.info/blog/simple-linear-regression-with-online-updates.html>`__
    """
    label = f"lag(input={input._label}, output={output._label})"
    nb_steps = len(time)
    slopes = [np.nan]
    lags = [np.nan]
    fitting_errors = [np.nan]
    dots = np.zeros(3)
    for i in range(nb_steps - 1):
        dt = time._values[i + 1] - time._values[i]
        if time_constant < 2 * dt:
            logging.warning(
                "Nyquist-Shannon sampling theorem: "
                "at time=%f, dt=%f but time_constant=%f",
                time._values[i],
                dt,
                time_constant,
            )
            slopes.append(np.nan)
            lags.append(np.nan)
            fitting_errors.append(np.nan)
            continue
        x = input._values[i] - output._values[i]
        y = output._values[i + 1] - output._values[i]
        if np.isnan(dt) or np.isnan(x) or np.isnan(y):
            slopes.append(np.nan)
            lags.append(np.nan)
            fitting_errors.append(np.nan)
            continue
        forgetting_factor = np.exp(-dt / time_constant)
        dots = forgetting_factor * dots + np.array([x * x, x * y, y * y])
        dot_xx = dots[0]
        if dot_xx < 1e-10:
            slopes.append(np.nan)
            lags.append(np.nan)
            fitting_errors.append(np.nan)
            continue
        dot_xy = dots[1]
        slope = dot_xy / dot_xx
        if slope < 1e-10 or slope > 0.9999999999:
            dots *= 0.0
            slopes.append(np.nan)
            lags.append(np.nan)
            fitting_errors.append(np.nan)
            continue
        # slope = 1.0 - exp(-dt / lag)
        lag = -dt / np.log(1.0 - slope)
        dot_yy = dots[2]
        total_error = slope**2 * dot_xx - 2 * dot_xy * slope + dot_yy
        # forgetting factor is exp(-dt / time_constant)
        normalizing_constant = 1.0 - forgetting_factor
        fitting_error = normalizing_constant * total_error
        slopes.append(slope)
        lags.append(lag)
        fitting_errors.append(fitting_error)
    node = Node(label)
    children = {
        "fitting_error": np.array(fitting_errors),
        "lag": np.array(lags),
        "slope": np.array(slopes),
    }
    node.__dict__.update(
        {
            key: Series(f"{label}/{key}", values=value, times=time._values)
            for key, value in children.items()
        }
    )
    return node
