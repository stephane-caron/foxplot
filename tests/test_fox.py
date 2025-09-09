#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

import json
import os
import tempfile
import unittest

import numpy as np
from foxplot.exceptions import FoxplotError
from foxplot.fox import Fox
from foxplot.series import Series


class TestFox(unittest.TestCase):
    def test_plot(self):
        fox = Fox.empty()
        fox.unpack({"time": 0.0, "foo": 1.0})
        fox.unpack({"time": 1.0, "foo": 1.0})
        fox.unpack({"time": 2.0, "foo": 1.0})
        fox.data._freeze(fox.length)
        fox.set_time(fox.data.time)
        fox.plot(left=[fox.data.foo])

    def test_unpack(self):
        custom_dict = {
            "action": {
                "servo": {
                    "left_hip": {"position": 0.0, "velocity": 0.0},
                    "left_knee": {"position": 0.0, "velocity": 0.0},
                    "left_wheel": {
                        "position": None,
                        "velocity": -1.7930299043655396,
                    },
                    "right_hip": {"position": 0.0, "velocity": 0.0},
                    "right_knee": {"position": 0.0, "velocity": 0.0},
                    "right_wheel": {
                        "position": None,
                        "velocity": 1.7930299043655396,
                    },
                }
            },
            "observation": {
                "cpu_temperature": 27.8,
                "floor_contact": {
                    "contact": False,
                    "left_wheel": {
                        "abs_acceleration": 0.0,
                        "abs_torque": 0.0,
                        "contact": False,
                        "inertia": 0.0,
                    },
                    "right_wheel": {
                        "abs_acceleration": 0.0,
                        "abs_torque": 0.0,
                        "contact": False,
                        "inertia": 0.0,
                    },
                    "upper_leg_torque": 0.3322237136603652,
                },
                "imu": {
                    "angular_velocity": [
                        9.68655861081597e-6,
                        0.01613060794484459,
                        -0.00002473763925328082,
                    ],
                    "linear_acceleration": [
                        0.005171997182880504,
                        -5.183437166339254e-6,
                        -0.00038763085867866525,
                    ],
                    "orientation": [
                        9.514175872027408e-6,
                        -0.002763640135526657,
                        1.0347052921133582e-6,
                        0.9999961853027344,
                    ],
                },
                "servo": {
                    "left_hip": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": -1.4625170398116709e-6,
                        "q_current": None,
                        "temperature": None,
                        "torque": 0.1569170987413283,
                        "velocity": -4.5614090602232155e-6,
                        "voltage": None,
                    },
                    "left_knee": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": -0.0001420909954679049,
                        "q_current": None,
                        "temperature": None,
                        "torque": 0.17143516145715895,
                        "velocity": -0.00043817754293275457,
                        "voltage": None,
                    },
                    "left_wheel": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": 0.0030391699212695533,
                        "q_current": None,
                        "temperature": None,
                        "torque": -0.19234722916873112,
                        "velocity": 0.01288744410063614,
                        "voltage": None,
                    },
                    "right_hip": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": 0.00009083758533694371,
                        "q_current": None,
                        "temperature": None,
                        "torque": -0.16313903364753277,
                        "velocity": 0.0003612714514143872,
                        "voltage": None,
                    },
                    "right_knee": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": -0.000021472875791296815,
                        "q_current": None,
                        "temperature": None,
                        "torque": -0.17344135560141116,
                        "velocity": -0.00012603570586484214,
                        "voltage": None,
                    },
                    "right_wheel": {
                        "d_current": None,
                        "fault": 0,
                        "mode": 0,
                        "position": -0.002959517382001668,
                        "q_current": None,
                        "temperature": None,
                        "torque": 0.19046651217002405,
                        "velocity": -0.01248384861209045,
                        "voltage": None,
                    },
                },
                "time": 1681318144.753685,
                "wheel_odometry": {"position": 0.0, "velocity": 0.0},
            },
            "policy": {
                "action": [-0.10758179426193237],
                "observation": [
                    -0.005527287255972624,
                    0.0,
                    0.0,
                    0.016130607575178146,
                ],
            },
            "time": 1681318144.751641,
        }
        fox = Fox.empty()
        fox.unpack(custom_dict)
        custom_dict["time"] += 1.0
        fox.unpack(custom_dict)
        custom_dict["time"] += 1.0
        fox.unpack(custom_dict)

    def test_missing_values(self):
        custom_dict = {
            "action": {
                "servo": {
                    "left_hip": {"position": 0.0, "velocity": 0.0},
                    "left_knee": {"position": 0.0, "velocity": 0.0},
                    "left_wheel": {
                        "position": None,
                        "velocity": -1.7930299043655396,
                    },
                    "right_hip": {"position": 0.0, "velocity": 0.0},
                    "right_knee": {"position": 0.0, "velocity": 0.0},
                    "right_wheel": {
                        "position": None,
                        "velocity": 1.7930299043655396,
                    },
                }
            },
            "time": 1681318144.751641,
        }
        fox = Fox.empty()
        fox.unpack(custom_dict)
        custom_dict["time"] += 1.0
        fox.unpack(custom_dict)

        old_action = custom_dict["action"]
        custom_dict["action"] = None  # missing value
        custom_dict["time"] += 1.0
        fox.unpack(custom_dict)

        custom_dict["action"] = old_action
        custom_dict["time"] += 1.0
        fox.unpack(custom_dict)

    def test_repeat_last_on_missing_1(self):
        fox = Fox.empty()
        config_a = 12345
        fox.unpack({"config_a": config_a, "time": 0.0})
        fox.data._freeze(1)
        self.assertEqual(fox.data.config_a._values.tolist(), [config_a])

    def test_repeat_last_on_missing_2(self):
        fox = Fox.empty()
        config_a = 12345
        fox.unpack({"config_a": config_a, "time": 0.0})
        fox.unpack({"x": 12, "time": 1.0})
        fox.data._freeze(2)
        self.assertEqual(fox.data.config_a._values.tolist(), [config_a] * 2)
        self.assertTrue(np.isnan(fox.data.x._values[0]))
        self.assertTrue(np.allclose(fox.data.x._values[1:], [12.0]))

    def test_repeat_last_on_missing_3(self):
        fox = Fox.empty()
        config_a = 12345
        fox.unpack({"config_a": config_a, "time": 0.0})
        fox.unpack({"x": 12, "time": 1.0})
        fox.unpack({"x": 22, "time": 2.0})
        fox.data._freeze(3)
        self.assertEqual(fox.data.config_a._values.tolist(), [config_a] * 3)
        self.assertTrue(np.isnan(fox.data.x._values[0]))
        self.assertTrue(np.allclose(fox.data.x._values[1:], [12.0, 22.0]))

    def test_repeat_last_on_missing_4(self):
        fox = Fox.empty()
        config_a = 12345
        fox.unpack({"config_a": config_a, "time": 0.0})
        fox.unpack({"x": 12, "time": 1.0})
        fox.unpack({"x": 22, "time": 2.0})
        fox.unpack({"x": 32, "time": 3.0})
        fox.data._freeze(4)
        self.assertEqual(fox.data.config_a._values.tolist(), [config_a] * 4)
        self.assertTrue(np.isnan(fox.data.x._values[0]))
        self.assertTrue(
            np.allclose(fox.data.x._values[1:], [12.0, 22.0, 32.0])
        )

    def test_constructor_with_file(self):
        # Test loading from a file
        data = [{"time": 0.0, "value": 1.0}, {"time": 1.0, "value": 2.0}]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
            temp_filename = f.name

        try:
            fox = Fox(temp_filename)
            self.assertEqual(fox.length, 2)
            self.assertTrue(hasattr(fox.data, "time"))
            self.assertTrue(hasattr(fox.data, "value"))
        finally:
            os.unlink(temp_filename)

    def test_detect_time_with_time_key(self):
        fox = Fox.empty()
        fox.unpack({"time": 0.0, "foo": 1.0})
        fox.unpack({"time": 1.0, "foo": 2.0})
        fox.data._freeze(fox.length)

        # Test detect_time finds 'time' key
        fox.detect_time()
        self.assertIsNotNone(fox._Fox__times)
        self.assertEqual(len(fox._Fox__times), 2)

    def test_detect_time_with_timestamp_key(self):
        fox = Fox.empty()
        fox.unpack({"timestamp": 0.0, "foo": 1.0})
        fox.unpack({"timestamp": 1.0, "foo": 2.0})
        fox.data._freeze(fox.length)

        # Test detect_time finds 'timestamp' key
        fox.detect_time()
        self.assertIsNotNone(fox._Fox__times)
        self.assertEqual(len(fox._Fox__times), 2)

    def test_detect_time_no_time_key(self):
        fox = Fox.empty()
        fox.unpack({"foo": 1.0})
        fox.data._freeze(fox.length)

        # Test detect_time when no time key is found
        fox.detect_time()
        self.assertIsNone(fox._Fox__times)

    def test_get_series_valid_label(self):
        fox = Fox.empty()
        fox.unpack({"nested": {"value": 1.0}})
        fox.data._freeze(fox.length)

        series = fox.get_series("/nested/value")
        self.assertIsInstance(series, Series)
        self.assertEqual(series._values[0], 1.0)

    def test_get_series_invalid_label(self):
        fox = Fox.empty()
        fox.unpack({"nested": {"value": 1.0}})
        fox.data._freeze(fox.length)

        with self.assertRaises(FoxplotError):
            fox.get_series("/nested")  # This is a Node, not a Series

    def test_plot_with_right_axis(self):
        fox = Fox.empty()
        fox.unpack({"time": 0.0, "left_val": 1.0, "right_val": 10.0})
        fox.unpack({"time": 1.0, "left_val": 2.0, "right_val": 20.0})
        fox.data._freeze(fox.length)
        fox.set_time(fox.data.time)

        # Test plotting with both left and right axes
        fox.plot(left=[fox.data.left_val], right=[fox.data.right_val])

    def test_plot_with_single_series(self):
        fox = Fox.empty()
        fox.unpack({"time": 0.0, "value": 1.0})
        fox.unpack({"time": 1.0, "value": 2.0})
        fox.data._freeze(fox.length)
        fox.set_time(fox.data.time)

        # Test plotting with single series (not in list)
        fox.plot(left=fox.data.value)
        fox.plot(left=fox.data.value, right=fox.data.value)

    def test_plot_with_custom_title(self):
        fox = Fox.empty()
        fox.unpack({"time": 0.0, "value": 1.0})
        fox.data._freeze(fox.length)
        fox.set_time(fox.data.time)

        fox.plot(left=[fox.data.value], title="Custom Title")

    def test_plot_with_node_expansion(self):
        fox = Fox.empty()
        fox.unpack({"nested": {"a": 1.0, "b": 2.0}, "time": 0.0})
        fox.unpack({"nested": {"a": 3.0, "b": 4.0}, "time": 1.0})
        fox.data._freeze(fox.length)
        fox.set_time(fox.data.time)

        # Test plotting with Node (should expand to its children)
        fox.plot(left=[fox.data.nested])

    def test_list_to_dict_with_invalid_type(self):
        fox = Fox.empty()
        fox.unpack({"value": 1.0})
        fox.data._freeze(fox.length)

        # Test __list_to_dict with invalid type
        with self.assertRaises(TypeError):
            fox._Fox__list_to_dict(["invalid_type"])

    def test_list_to_dict_with_nested_non_series(self):
        fox = Fox.empty()
        fox.unpack({"deep": {"nested": {"value": 1.0}}})
        fox.data._freeze(fox.length)

        # This should trigger the warning for non-series children
        result = fox._Fox__list_to_dict([fox.data.deep])
        # The warning should be logged, but we can't easily test that
        self.assertIsInstance(result, dict)

    def test_plot_without_time_index(self):
        fox = Fox.empty()
        fox.unpack({"value": 1.0})
        fox.unpack({"value": 2.0})
        fox.data._freeze(fox.length)

        # Plot without setting time index (should use indices)
        fox.plot(left=[fox.data.value])

    def test_source_attribute(self):
        fox = Fox.empty()
        self.assertEqual(fox._Fox__source, "custom data")

        # Test with filename
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False
        ) as f:
            f.write('{"time": 0.0}\n')
            temp_filename = f.name

        try:
            fox_with_file = Fox(temp_filename)
            self.assertEqual(fox_with_file._Fox__source, temp_filename)
        finally:
            os.unlink(temp_filename)
