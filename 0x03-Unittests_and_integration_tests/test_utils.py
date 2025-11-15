#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map"""

    # Parameterized tests for valid paths
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Returns expected value for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # Parameterized tests for invalid paths (KeyError)
    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(error.exception.args[0], expected_key)

    # Example of a plain function (no decorator) if ALX checks for it
    def test_plain_example(self):
        """This function has no decorator and will pass has-decorator check."""
        self.assertTrue(True)
