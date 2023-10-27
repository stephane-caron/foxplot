#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

import os

from foxplot import Fox

if __name__ == "__main__":
    curdir = os.path.dirname(os.path.abspath(__file__))
    fox = Fox(from_file=f"{curdir}/robot_data.json", time="time")
    action = fox.data.action
    observation = fox.data.observation
    fox.plot(
        left=[
            action.wheel_balancer.ground_velocity,
            observation.wheel_odometry.velocity,
        ],
        right=[observation.servo.left_wheel.velocity],
    )
