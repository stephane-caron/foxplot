#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

"""Pick plot colors from a circular list."""

from typing import List


class ColorPicker:
    """Pick from a circular list of color strings."""

    COLORS: List[str] = [
        "red",
        "green",
        "blue",
        "magenta",
        "orange",
        "cyan",
        "purple",
        "lime",
        "#AABBCC",
        "#BBAACC",
        "#CCBBAA",
        "#AABBAA",
    ]

    def __init__(self):
        """Initialize color picker."""
        self.reset()

    def get_next_color(self) -> str:
        """Get next color in the list.

        Returns:
            Color string.
        """
        color = self.COLORS[self.__next_color]
        self.__next_color += 1
        return color

    def reset(self) -> None:
        """Reset picker to the first color."""
        self.__next_color = 0
