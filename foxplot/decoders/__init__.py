#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Decoder functions."""

from .json import decode_json
from .msgpack import decode_msgpack

__all__ = [
    "decode_json",
    "decode_msgpack",
]
