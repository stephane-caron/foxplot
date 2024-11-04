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
    """Unpack a series of dictionaries from a given file.

    Args:
        filename: Name of a file to read time series from (can be "stdin").

    Yields:
        Unpacked dictionaries.
    """
    if filename == "stdin":
        yield from decode_json(file=sys.stdin)
    elif filename.endswith(".json"):
        with open(filename, "r", encoding="utf-8") as file:
            yield from decode_json(file=file)
    elif filename.endswith(".mpack"):
        with open(filename, "rb") as file:
            yield from decode_msgpack(file=file)
    else:  # unknown file extension
        raise FoxplotError(f"Unknown file type in '{filename}'")
