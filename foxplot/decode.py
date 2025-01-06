#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Decode a series of dictionaries from file."""

import sys
from pathlib import PosixPath
from typing import Generator, Union

from .decoders.json import decode_json
from .decoders.msgpack import decode_msgpack
from .exceptions import FoxplotError


def decode(file_path: Union[str, PosixPath]) -> Generator[dict, None, None]:
    """Unpack a series of dictionaries from a given file.

    Args:
        file_path: Path to the file to read from (can be "stdin").

    Yields:
        Unpacked dictionaries.
    """
    file_path = str(file_path)
    if file_path == "stdin":
        yield from decode_json(file=sys.stdin)
    elif file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as file:
            yield from decode_json(file=file)
    elif file_path.endswith(".mpack"):
        with open(file_path, "rb") as file:
            yield from decode_msgpack(file=file)
    else:  # unknown file extension
        raise FoxplotError(f"Unknown file type in '{file_path}'")
