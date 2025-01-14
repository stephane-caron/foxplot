#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

import unittest

import numpy as np

from foxplot.fox import Fox


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
