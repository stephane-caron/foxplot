#!/usr/bin/env python3
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
