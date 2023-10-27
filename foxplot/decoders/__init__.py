#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
# SPDX-License-Identifier: Apache-2.0

"""Decoder functions."""

from .json import decode_json
from .msgpack import decode_msgpack

__all__ = [
    "decode_json",
    "decode_msgpack",
]
