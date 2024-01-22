#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""Decoder function for MessagePack."""

from typing import Generator

import msgpack


def decode_msgpack(file, chunk_size=100_000) -> Generator[dict, None, None]:
    """Decode dictionaries from a line-delimited JSON file.

    Args:
        file: File stream (for instance ``sys.stdin``).
        chunk_size: Number of bytes read at a time from the standard input.

    Yields:
        dict: Dictionary read from the standard input.
    """
    unpacker = msgpack.Unpacker(raw=False)
    while True:
        data = file.read(chunk_size)
        if not data:  # end of file
            break
        unpacker.feed(data)
        for unpacked in unpacker:
            yield unpacked
