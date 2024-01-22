#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Decoder functions."""

import json
from typing import Generator


def decode_json(file, chunk_size=100_000) -> Generator[dict, None, None]:
    """Decode dictionaries from a line-delimited JSON file.

    Args:
        file: File stream (for instance ``sys.stdin``).
        chunk_size: Number of bytes read at a time from the standard input.

    Yields:
        dict: Dictionary read from the standard input.
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
