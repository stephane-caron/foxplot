#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Decode a series of dictionaries from file."""

import json
import sys
from pathlib import PosixPath
from typing import Generator, Union

import mpacklog

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
    elif file_path.endswith(".json") or file_path.endswith(".jsonl"):
        with open(file_path, "r", encoding="utf-8") as file:
            yield from decode_json(file=file)
    elif file_path.endswith(".mpack"):
        yield from mpacklog.read_log(file_path)
    else:  # unknown file extension
        raise FoxplotError(f"Unknown file type in '{file_path}'")


def decode_json(file, chunk_size=100_000) -> Generator[dict, None, None]:
    """Decode dictionaries from a line-delimited JSON file.

    Args:
        file: File stream (for instance ``sys.stdin``).
        chunk_size: Number of bytes read at a time from the standard input.

    Yields:
        dict: Dictionary read from file.
    """
    decoder = json.JSONDecoder()
    buffer = ""
    while True:
        data = file.read(chunk_size)
        if not data:  # end of file
            break
        buffer += data
        while buffer:
            try:
                result, index = decoder.raw_decode(buffer)
                buffer = buffer[index:].lstrip()
                yield result
            except json.JSONDecodeError:
                break
