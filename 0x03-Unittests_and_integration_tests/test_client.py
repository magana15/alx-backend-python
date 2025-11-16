#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.org.

"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
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

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the repos_url value obtained from
        the org payload.
        """
        payload = {"repos_url": "https://api.github.com/orgs/holberton/repos"}
        expected = payload["repos_url"]

        # Patch the org property on the class with a PropertyMock
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("holberton")
            result = client._public_repos_url

            self.assertEqual(result, expected)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the list of repo names
        obtained from get_json and that both _public_repos_url and get_json are
        called exactly once.
        """
        # Arrange: mock the URL property and the get_json return payload
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = repos_payload
        expected_url = "https://api.github.com/orgs/test/repos"
        expected_repos = ["repo1", "repo2"]

        # Patch the _public_repos_url property on the class
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = expected_url

            # Act: instantiate client and call public_repos
            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assert: return value is as expected
            self.assertEqual(result, expected_repos)

            # Assert: both the property and get_json were called once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
