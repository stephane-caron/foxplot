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

"""
Generate an HTML page containing the output plot.
"""

from math import isnan
from typing import Any, Dict, Iterable, List

from pkg_resources import resource_filename

from .color_picker import ColorPicker


def __escape_null(series: Iterable) -> str:
    """
    Escape undefined values in a series.

    Args:
        series: Series to filter.

    Returns:
        String representation of the series.
    """
    return (
        "["
        + ", ".join(
            map(
                lambda x: str(int(x))
                if isinstance(x, bool)
                else str(x)
                if isinstance(x, (int, float)) and not isnan(x)
                else x
                if isinstance(x, str)
                else "null",
                series,
            )
        )
        + "]"
    )


def generate_html(
    title: str,
    series: Dict[str, Any],
    left_axis_fields: List[str],
    right_axis_fields: List[str],
    left_axis_unit: str = "",
    right_axis_unit: str = "",
) -> str:
    """
    Generate plot in an HTML page.

    Args:
        title:

    Returns:
        HTML contents of the page.
    """
    color_picker = ColorPicker()
    left_axis_label = f" {left_axis_unit}" if left_axis_unit else ""
    right_axis_label = f" {right_axis_unit}" if right_axis_unit else ""
    fields = left_axis_fields + right_axis_fields  # keep CLI ordering
    right_axis_set = set(right_axis_fields)  # for faster queries below
    uplot_min_css = resource_filename("foxplot", "uPlot/uPlot.min.css")
    uplot_iife_js = resource_filename("foxplot", "uPlot/uPlot.iife.js")
    uplot_mwheel_js = resource_filename("foxplot", "uPlot/uPlot.mousewheel.js")
    if None in series["time"]:
        raise ValueError("time series cannot contain None values")
    html = f"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{uplot_min_css}">
        <style>
            div.my-chart {{
                background-color: white;
                padding: 10px 0px;  // appear in Right Click -> Take Screenshot
            }}
        </style>
    </head>
    <body>
        <script src="{uplot_iife_js}"></script>
        <script src="{uplot_mwheel_js}"></script>
        <script>
            const {{ linear, stepped, bars, spline, spline2 }} = uPlot.paths;

            let data = [
                {series["time"]},"""
    for field in fields:
        html += f"""
                {__escape_null(series[field])},"""
    html += """
            ];

            const lineInterpolations = {
                linear: 0,
                stepAfter: 1,
                stepBefore: 2,
                spline: 3,
            };

            const _stepBefore = stepped({align: -1});
            const _stepAfter = stepped({align:  1});
            const _linear = linear();
            const _spline = spline();

            function paths(u, seriesIdx, idx0, idx1, extendGap, buildClip) {
                let s = u.series[seriesIdx];
                let interp = s.lineInterpolation;

                let renderer = (
                    interp == lineInterpolations.linear ? _linear :
                    interp == lineInterpolations.stepAfter ? _stepAfter :
                    interp == lineInterpolations.stepBefore ? _stepBefore :
                    interp == lineInterpolations.spline ? _spline :
                    null
                );

                return renderer(
                    u, seriesIdx, idx0, idx1, extendGap, buildClip
                );
            }

            let opts = {"""
    html += f"""
                title: "{title}","""
    html += """
                id: "chart1",
                class: "my-chart",
                width: window.innerWidth - 20,
                height: window.innerHeight - 150,
                cursor: {
                    drag: {
                        x: true,
                        y: true,
                        uni: 50,
                    }
                },
                plugins: [
                    wheelZoomPlugin({factor: 0.75})
                ],
                scales: {
                    x: {
                        time: true,
                    },
                },
                series: ["""
    html += f"""
                    {{
                        value: (self, rawValue) => Number.parseFloat(rawValue -
                        {series["time"][0]}).toPrecision(3),
                    }},"""
    for field in fields:
        html += f"""
                    {{
                        // initial toggled state (optional)
                        show: true,
                        spanGaps: false,

                        // in-legend display
                        label: "{field}","""
        if field in right_axis_set:
            html += f"""
                        value: (self, rawValue) =>
                            Number.parseFloat(rawValue).toPrecision(2) +
                            "{right_axis_label}",
                        scale: "{right_axis_unit}","""
        else:  # field in left_axis_fields
            html += f"""
                        value: (self, rawValue) =>
                            Number.parseFloat(rawValue).toPrecision(2) +
                            "{left_axis_label}","""
        html += f"""
                        // series style
                        stroke: "{color_picker.get_next_color()}",
                        width: 2 / devicePixelRatio,
                        lineInterpolation: lineInterpolations.stepAfter,
                        paths,
                    }},"""
    html += """
                ],
                axes: [
                    {},
                    {"""
    html += f"""
                        size: {60 + 10 * len({left_axis_label})},
                        values: (u, vals, space) => vals.map(
                            v => v + "{left_axis_label}"
                        ),"""
    html += """
                    },
                    {
                        side: 1,"""
    html += f"""
                        scale: "{right_axis_unit}",
                        size: {60 + 10 * len({right_axis_label})},
                        values: (u, vals, space) => vals.map(
                            v => v + "{right_axis_label}"
                        ),"""
    html += """
                        grid: {show: false},
                    },
                ],
            };

            let uplot = new uPlot(opts, data, document.body);

            // resize with window
            window.addEventListener("resize", e => {
                uplot.setSize({
                    width: window.innerWidth - 20,
                    height: window.innerHeight - 150,
                });
            });
        </script>
    </body>
</html>"""
    return html