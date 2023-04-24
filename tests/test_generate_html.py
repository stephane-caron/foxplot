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


class TestGenerateHtml(unittest.TestCase):
    def test_generate_html(self):
        times = [1.0, 2.0, 0.0]
        label = "my_left_axis_foo"
        html = generate_html(
            times,
            left_axis={label: [0.0, 1.0, -1.0]},
            right_axis={},
            title="Test",
        )
        self.assertIn(label, html)
        self.assertIn(f'label: "{label}"', html)
