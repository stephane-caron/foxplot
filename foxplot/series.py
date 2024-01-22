#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023-2024 Inria

"""Series data unpacked from input dictionaries."""

import abc
from typing import List


class Series:
    """Base class for labeled time series."""

    _label: str

    def __init__(self, label: str):
        """Initialize a new indexed series.

        Args:
            label: Label of the series in the input data.
        """
        self._label = label

    @abc.abstractmethod
    def __len__(self):
        """Length of the indexed series."""

    @abc.abstractmethod
    def __repr__(self):
        """String representation of the series."""

    def _list_labels(self) -> List[str]:
        """List all labels reachable from this node.

        Returns:
            List of labels. Since this node is a leaf, there is only one.
        """
        return [self._label]
