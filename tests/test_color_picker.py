#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

import unittest

from foxplot.color_picker import ColorPicker


class TestColorPicker(unittest.TestCase):
    def test_color_picker(self):
        picker = ColorPicker()
        first_color = picker.get_next_color()
        second_color = picker.get_next_color()
        self.assertNotEqual(first_color, second_color)

        picker.reset()
        reset_color = picker.get_next_color()
        self.assertEqual(first_color, reset_color)
