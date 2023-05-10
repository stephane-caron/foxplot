#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

"""Plot time series."""

import tempfile
from datetime import datetime


def write_tmpfile(html: str) -> str:
    """Write output page.

    Args:
        html: HTML content.

    Returns:
        Name of the output file (a temporary file).
    """
    filename: str = ""
    with tempfile.NamedTemporaryFile(
        mode="w+",
        prefix=f"plot-{datetime.now().strftime('%Y%m%d-%H%M%S')}-",
        suffix=".html",
        delete=False,
    ) as output_file:
        output_file.write(html)
        filename = f"file://{output_file.name}"
    return filename
