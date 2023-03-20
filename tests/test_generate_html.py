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

import unittest

from foxplot.generate_html import generate_html
from foxplot.series import Series


class TestGenerateHtml(unittest.TestCase):
    def test_generate_html(self):
        generate_html(
            Series(
                index=None,
                left_axis_fields=[],
                right_axis_fields=[],
                timestamped=False,
            ),
            "Test",
        )
