#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.org.

"""

import unittest
from parameterized import parameterized
from unittest.mock import patch

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, mock_get_json, org_name):
        """
        Test that GithubOrgClient.org returns the value returned by get_json
        and is called exactly once with correct URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
