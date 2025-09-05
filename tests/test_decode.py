#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

import json
import tempfile
import unittest
from unittest.mock import patch, mock_open
import sys

import msgpack

from foxplot.decoders import decode_json, decode_msgpack
from foxplot.decode import decode
from foxplot.exceptions import FoxplotError


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


class TestDecode(unittest.TestCase):
    def test_decode_stdin(self):
        test_data = '{"a": 1}\n{"b": 2}\n'
        with patch.object(sys, 'stdin', mock_open(read_data=test_data).return_value):
            result = list(decode("stdin"))
            self.assertEqual(result, [{"a": 1}, {"b": 2}])

    def test_decode_json_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            f.flush()
            result = list(decode(f.name))
            self.assertEqual(result, [{"test": "data"}])

    def test_decode_jsonl_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write('{"a": 1}\n{"b": 2}\n')
            f.flush()
            result = list(decode(f.name))
            self.assertEqual(result, [{"a": 1}, {"b": 2}])

    def test_decode_msgpack_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".mpack", delete=False) as f:
            msgpack.pack({"test": "data"}, f)
            f.flush()
            result = list(decode(f.name))
            self.assertEqual(result, [{"test": "data"}])

    def test_decode_unknown_extension(self):
        with self.assertRaises(FoxplotError) as cm:
            list(decode("test.unknown"))
        self.assertIn("Unknown file type", str(cm.exception))
