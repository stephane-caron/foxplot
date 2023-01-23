#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
