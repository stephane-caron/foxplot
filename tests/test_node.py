#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

import unittest

import numpy as np
from foxplot.exceptions import FoxplotError
from foxplot.hot_series import HotSeries
from foxplot.node import Node
from foxplot.series import Series


class TestNode(unittest.TestCase):
    def test_init(self):
        node = Node("/test")
        self.assertEqual(node._label, "/test")

    def test_getitem(self):
        node = Node("/")
        node.child = "value"
        self.assertEqual(node["child"], "value")

    def test_repr_empty_node(self):
        node = Node("/test")
        result = repr(node)
        self.assertEqual(result, "/test: []")

    def test_repr_with_children(self):
        node = Node("/test")
        node.child1 = "value1"
        node.child2 = "value2"
        result = repr(node)
        self.assertIn("/test: [", result)
        self.assertIn("child1", result)
        self.assertIn("child2", result)

    def test_repr_with_private_attributes(self):
        node = Node("/test")
        node._private = "should not appear"
        node.public = "should appear"
        result = repr(node)
        self.assertIn("public", result)
        self.assertNotIn("_private", result)

    def test_repr_with_integer_keys(self):
        node = Node("/test")
        node.__dict__[0] = "indexed_value"
        node.regular = "regular_value"
        result = repr(node)
        self.assertIn("0", result)
        self.assertIn("regular", result)

    def test_get_child_single_key(self):
        node = Node("/")
        values = np.array([1.0, 2.0])
        times = np.array([0.0, 1.0])
        series = Series("/child", values, times)
        node.child = series

        result = node._get_child(["child"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result._label, "/child")

    def test_get_child_nested_keys(self):
        root = Node("/")
        middle = Node("/middle")
        values = np.array([1.0, 2.0])
        times = np.array([0.0, 1.0])
        leaf = Series("/middle/leaf", values, times)

        middle.leaf = leaf
        root.middle = middle

        result = root._get_child(["middle", "leaf"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result._label, "/middle/leaf")

    def test_get_child_non_series_leaf(self):
        node = Node("/")
        child_node = Node("/child")
        node.child = child_node

        with self.assertRaises(FoxplotError):
            node._get_child(["child"])

    def test_items(self):
        node = Node("/test")
        node.child1 = "value1"
        node.child2 = "value2"
        node._private = "private_value"

        items = list(node._items())
        keys = [key for key, _ in items]

        self.assertIn("child1", keys)
        self.assertIn("child2", keys)
        self.assertNotIn("_private", keys)

    def test_items_with_integer_keys(self):
        node = Node("/test")
        node.__dict__[0] = "indexed_value"
        node.__dict__[1] = "another_indexed"
        node.regular = "regular_value"

        items = list(node._items())
        keys = [key for key, _ in items]

        self.assertIn(0, keys)
        self.assertIn(1, keys)
        self.assertIn("regular", keys)

    def test_list_labels_empty(self):
        node = Node("/test")
        labels = node._list_labels()
        self.assertEqual(labels, [])

    def test_list_labels_with_children(self):
        root = Node("/")
        values1 = np.array([1.0])
        times1 = np.array([0.0])
        child1 = Series("/child1", values1, times1)
        child2 = Node("/child2")
        values2 = np.array([2.0])
        times2 = np.array([0.0])
        nested_series = Series("/child2/nested", values2, times2)

        child2.nested = nested_series
        root.child1 = child1
        root.child2 = child2

        labels = root._list_labels()
        self.assertIn("/child1", labels)
        self.assertIn("/child2/nested", labels)

    def test_list_labels_skips_private_and_integers(self):
        node = Node("/")
        values = np.array([1.0])
        times = np.array([0.0])
        node._private_child = Series("/private", values, times)
        node.__dict__[0] = Series("/indexed", values, times)
        public_series = Series("/public", values, times)
        node.public = public_series

        labels = node._list_labels()
        self.assertIn("/public", labels)
        self.assertNotIn("/private", labels)
        self.assertEqual(len(labels), 1)

    def test_update_with_none(self):
        node = Node("/test")
        node._update(0, None)
        # Should not crash and should not add any children
        self.assertEqual(
            len([k for k in node.__dict__ if not k.startswith("_")]), 0
        )

    def test_update_with_dict(self):
        node = Node("/")
        data = {"key1": "value1", "key2": {"nested": "nested_value"}}
        node._update(0, data)

        self.assertTrue(hasattr(node, "key1"))
        self.assertTrue(hasattr(node, "key2"))
        self.assertIsInstance(node.key1, HotSeries)
        self.assertIsInstance(node.key2, Node)

    def test_update_with_list(self):
        node = Node("/")
        data = ["item0", "item1"]
        node._update(0, data)

        self.assertTrue(hasattr(node, "__dict__"))
        self.assertIn(0, node.__dict__)
        self.assertIn(1, node.__dict__)
        self.assertIsInstance(node.__dict__[0], HotSeries)
        self.assertIsInstance(node.__dict__[1], HotSeries)

    def test_update_existing_child(self):
        node = Node("/")
        existing_series = HotSeries("/existing")
        node.existing = existing_series

        # Update with new value
        node._update(0, {"existing": "new_value"})
        # Should still be the same object
        self.assertIs(node.existing, existing_series)

    def test_freeze_with_hot_series(self):
        node = Node("/")
        hot = HotSeries("/hot")
        hot._update(0, 1.0)
        hot._update(1, 2.0)
        node.hot = hot

        node._freeze(2)

        # HotSeries should be converted to Series
        self.assertIsInstance(node.hot, Series)
        np.testing.assert_array_equal(node.hot._values, [1.0, 2.0])

    def test_freeze_with_nested_nodes(self):
        root = Node("/")
        child = Node("/child")
        hot = HotSeries("/child/hot")
        hot._update(0, 5.0)
        child.hot = hot
        root.child = child

        root._freeze(1)

        # Nested HotSeries should be converted
        self.assertIsInstance(root.child.hot, Series)
        np.testing.assert_array_equal(root.child.hot._values, [5.0])

    def test_freeze_mixed_children(self):
        node = Node("/")
        hot1 = HotSeries("/hot1")
        hot1._update(0, 10.0)
        hot2 = HotSeries("/hot2")
        hot2._update(0, 20.0)
        child_node = Node("/child")

        node.hot1 = hot1
        node.hot2 = hot2
        node.child = child_node

        node._freeze(1)

        self.assertIsInstance(node.hot1, Series)
        self.assertIsInstance(node.hot2, Series)
        self.assertIsInstance(node.child, Node)  # Unchanged
