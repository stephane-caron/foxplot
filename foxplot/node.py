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

"""Internal node used to access data in interactive mode."""

from typing import List, Union

from .exceptions import FoxplotException
from .indexed_series import IndexedSeries


class Node:
    """Series data unpacked from input dictionaries."""

    __label: str

    def __init__(self, label: str):
        """Initialize node with a label.

        Args:
            label: Node label.
        """
        self.__label = label

    def __getitem__(self, key):
        """Get item from node, either a child node or an indexed series (leaf).

        Args:
            key: Key that identifies the child item.
        """
        return self.__dict__[key]

    def __repr__(self):
        """String representation of the node."""
        keys = ", ".join(
            str(key)
            for key in self.__dict__
            if isinstance(key, int) or not key.startswith("_")
        )
        return f"{self.__label}: [{keys}]"

    def _get_child(self, keys: List[str]) -> IndexedSeries:
        """Get leaf descendant in the tree from a list of keys.

        Args:
            keys: List of keys uniquely identifying the leaf descendant.
        """
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child._get_child(keys[1:])
        if not isinstance(child, IndexedSeries):
            raise FoxplotException(f"{child.label} is not a time series")
        return child

    def _list_labels(self) -> List[str]:
        """List all labels reachable from this node."""
        labels = []
        for key, child in self.__dict__.items():
            if isinstance(key, int) or key.startswith("_"):
                continue
            labels.extend(child._list_labels())
        return labels

    def _update(self, index: int, unpacked: Union[dict, list]) -> None:
        """Update node from a new unpacked dictionary.

        Args:
            index: Index of the unpacked dictionary in the sequential input.
            unpacked: Unpacked dictionary.
        """
        items = (
            unpacked.items()
            if isinstance(unpacked, dict)
            else enumerate(unpacked)
        )
        for key, value in items:
            if key in self.__dict__:
                child = self.__dict__[key]
            else:  # key not in self.__dict__
                sep = "/" if not self.__label.endswith("/") else ""
                child = (
                    Node if isinstance(value, (dict, list)) else IndexedSeries
                )(label=f"{self.__label}{sep}{key}")
                self.__dict__[key] = child
            child._update(index, value)
