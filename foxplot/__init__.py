#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron
# Copyright 2023-2024 Inria

"""Plot time-series data from line-delimited JSON."""

__version__ = "1.0.0"

from .decode import decode
from .fox import Fox

__all__ = [
    "Fox",
    "decode",
]
