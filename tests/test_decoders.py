#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
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

import json
import tempfile
import unittest

import msgpack

from foxplot.decoders import decode_json, decode_msgpack


class TestDecoders(unittest.TestCase):
    EXPECTED_DICTS = [
        {"a": 1, "b": 2},
        {"c": 3, "d": 4},
    ]

    def setUp(self):
        self.json_file = tempfile.NamedTemporaryFile(mode="w+")
        self.msgpack_file = tempfile.NamedTemporaryFile(mode="wb+")
        for d in self.EXPECTED_DICTS:
            self.json_file.file.write(json.dumps(d) + "\n")
            self.msgpack_file.file.write(msgpack.packb(d))
        self.json_file.file.seek(0)
        self.msgpack_file.file.seek(0)

    def tearDown(self):
        self.json_file.close()

    def test_decode_json(self):
        read_dicts = list(decode_json(file=self.json_file.file))
        for read, expected in zip(read_dicts, self.EXPECTED_DICTS):
            self.assertDictEqual(read, expected)

    def test_decode_msgpack(self):
        read_dicts = list(decode_msgpack(file=self.msgpack_file.file))
        for read, expected in zip(read_dicts, self.EXPECTED_DICTS):
            self.assertDictEqual(read, expected)
