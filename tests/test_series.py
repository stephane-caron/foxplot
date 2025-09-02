#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

import unittest

import numpy as np

from foxplot.exceptions import FoxplotError
from foxplot.series import Series


class TestSeries(unittest.TestCase):
    def setUp(self):
        times = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        # Instance attributes
        self.no_times_series = Series("no_times", values, None)
        self.series = Series("test", values, times)
        self.times = times
        self.values = values

    def test_add(self):
        other = Series(
            "other", np.array([1.0, 1.0, 1.0, 1.0, 1.0]), self.times
        )
        result = self.series + other
        np.testing.assert_array_equal(
            result._values, [2.0, 3.0, 4.0, 5.0, 6.0]
        )
        self.assertEqual(result._label, "(test + other)")

    def test_mul_series(self):
        other = Series(
            "other", np.array([2.0, 2.0, 2.0, 2.0, 2.0]), self.times
        )
        result = self.series * other
        np.testing.assert_array_equal(
            result._values, [2.0, 4.0, 6.0, 8.0, 10.0]
        )
        self.assertEqual(result._label, "(test * other)")

    def test_mul_scalar(self):
        result = self.series * 2.0
        np.testing.assert_array_equal(
            result._values, [2.0, 4.0, 6.0, 8.0, 10.0]
        )
        self.assertEqual(result._label, "(test * 2.0)")

    def test_truediv_series(self):
        other = Series(
            "other", np.array([2.0, 2.0, 2.0, 2.0, 2.0]), self.times
        )
        result = self.series / other
        np.testing.assert_array_equal(
            result._values, [0.5, 1.0, 1.5, 2.0, 2.5]
        )
        self.assertEqual(result._label, "(test / other)")

    def test_truediv_scalar(self):
        result = self.series / 2.0
        np.testing.assert_array_equal(
            result._values, [0.5, 1.0, 1.5, 2.0, 2.5]
        )
        self.assertEqual(result._label, "(test / 2.0)")

    def test_neg(self):
        result = -self.series
        np.testing.assert_array_equal(
            result._values, [-1.0, -2.0, -3.0, -4.0, -5.0]
        )
        self.assertEqual(result._label, "-test")

    def test_len(self):
        self.assertEqual(len(self.series), 5)

    def test_repr(self):
        result = repr(self.series)
        self.assertIn("Time series with values:", result)

    def test_abs(self):
        negative_series = Series(
            "neg", np.array([-1.0, -2.0, 3.0]), self.times[:3]
        )
        result = negative_series.abs()
        np.testing.assert_array_equal(result._values, [1.0, 2.0, 3.0])
        self.assertEqual(result._label, "abs(neg)")

    def test_deriv_no_times_error(self):
        with self.assertRaises(FoxplotError) as cm:
            self.no_times_series.deriv("s")
        self.assertIn("Unset time values", str(cm.exception))

    def test_deriv_basic(self):
        result = self.series.deriv("s")
        expected_values = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        np.testing.assert_allclose(result._values, expected_values)
        self.assertEqual(result._label, "deriv(test, unit=s)")

    def test_deriv_with_cutoff(self):
        result = self.series.deriv("s", cutoff=0.5)
        self.assertIn("cutoff=0.5 s", result._label)

    def test_low_pass_filter_no_times_error(self):
        with self.assertRaises(FoxplotError) as cm:
            self.no_times_series.low_pass_filter(1.0)
        self.assertIn("Unset time values", str(cm.exception))

    def test_low_pass_filter(self):
        result = self.series.low_pass_filter(2.0)
        self.assertEqual(
            result._label, "low_pass_filter(test, cutoff_period=2.0)"
        )
        self.assertEqual(len(result._values), len(self.values))

    def test_std(self):
        result = self.series.std(3)
        self.assertEqual(result._label, "std(test, 3)")
        self.assertEqual(len(result._values), len(self.values) - 2)
