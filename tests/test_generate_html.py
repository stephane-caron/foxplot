#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

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
