#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""Internal node used to access data in interactive mode."""

from typing import Any, Dict, List, Union, cast

from .exceptions import FoxplotError
from .hot_series import HotSeries
from .series import Series


class Node:
    """Series data unpacked from input dictionaries."""

    _label: str

    def __init__(self, label: str):
        """Initialize node with a label.

        Args:
            label: Node label.
        """
        self._label = label

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
        return f"{self._label}: [{keys}]"

    def _get_child(self, keys: List[str]) -> Series:
        """Get leaf descendant in the tree from a list of keys.

        Args:
            keys: List of keys uniquely identifying the leaf descendant.
        """
        child = self.__dict__[keys[0]]
        if len(keys) > 1:
            return child._get_child(keys[1:])
        if not isinstance(child, Series):
            raise FoxplotError(f"{child._label} is not a time series")
        return child

    def _items(self):
        for key, child in self.__dict__.items():
            if isinstance(key, str) and key.startswith("_"):
                continue
            yield (key, child)

    def _list_labels(self) -> List[str]:
        """List all labels reachable from this node."""
        labels = []
        for key, child in self.__dict__.items():
            if isinstance(key, int) or key.startswith("_"):
                continue
            labels.extend(child._list_labels())
        return labels

    def _update(self, index: int, unpacked: Union[None, dict, list]) -> None:
        """Update node from a new unpacked dictionary.

        Args:
            index: Index of the unpacked dictionary in the sequential input.
            unpacked: Unpacked dictionary.
        """
        if unpacked is None:
            return
        items = (
            unpacked.items()
            if isinstance(unpacked, dict)
            else enumerate(unpacked)
        )
        for key, value in items:
            # Explicitly signal to the type checker that keys can be integers
            self_dict = cast(Dict[Union[str, int], Any], self.__dict__)
            if key in self.__dict__:
                child = self_dict[key]
            else:  # key not in self.__dict__
                sep = "/" if not self._label.endswith("/") else ""
                is_primitive = not isinstance(value, (dict, list))
                ChildClass = HotSeries if is_primitive else Node
                child = ChildClass(label=f"{self._label}{sep}{key}")
                self_dict[key] = child
            child._update(index, value)

    def _freeze(self, max_index: int) -> None:
        update = {}
        for key, child in self.__dict__.items():
            if isinstance(child, HotSeries):
                frozen_series = child._freeze(max_index)
                update[key] = frozen_series
            elif isinstance(child, Node):
                child._freeze(max_index)
        self.__dict__.update(update)
