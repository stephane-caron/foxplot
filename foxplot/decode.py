#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import sys

from .decoders.json import decode_json
from .decoders.msgpack import decode_msgpack
from .exceptions import FoxplotError


def decode(filename: str) -> None:
    """Unpack dictionaries series from file.

    Args:
        filename: Name of a file to read time series from.

    Yields:
        Unpacked dictionaries.
    """
    if filename == "stdin":
        for unpacked in decode_json(file=sys.stdin):
            yield unpacked
    elif filename.endswith(".json"):
        with open(filename, "r", encoding="utf-8") as file:
            for unpacked in decode_json(file=file):
                yield unpacked
    elif filename.endswith(".mpack"):
        with open(filename, "rb") as file:
            for unpacked in decode_msgpack(file=file):
                yield unpacked
    else:  # unknown file extension
        raise FoxplotError(f"Unknown file type in '{filename}'")
