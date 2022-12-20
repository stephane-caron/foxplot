#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron and the qpsolvers contributors.
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

import json
import tempfile
import unittest

from foxplot.decoders import decode_json


class TestDecoders(unittest.TestCase):

    """
    Test fixture for decoder functions.
    """

    EXPECTED_DICTS = [
        {"a": 1, "b": 2},
        {"c": 3, "d": 4},
    ]

    def setUp(self):
        self.json_file = tempfile.NamedTemporaryFile(mode="w+")
        for d in self.EXPECTED_DICTS:
            self.json_file.file.write(json.dumps(d) + "\n")
        self.json_file.file.seek(0)

    def tearDown(self):
        self.json_file.close()

    def test_decode_json(self):
        read_dicts = list(decode_json(file=self.json_file.file))
        for read, expected in zip(read_dicts, self.EXPECTED_DICTS):
            self.assertDictEqual(read, expected)
