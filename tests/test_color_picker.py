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
