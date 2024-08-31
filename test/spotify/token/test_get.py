"""Module to test the get method of the Spotify Token"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from time import time

from custom_components.spotcast.spotify.token import SpotifyToken


class TestTokenRefresh(TestCase):

    def setUp(self):
        self.token = SpotifyToken("12345", time() + 1000)

    @patch.object(SpotifyToken, "_refresh")
    def test_force_refresh(self, mock_refresh: MagicMock):

        mock_refresh.return_value = "1234", 3.1415

        self.token.get("foo", "bar", force=True)

        try:
            mock_refresh.assert_called()
        except AssertionError:
            self.fail("refresh method was not called")

    @patch.object(SpotifyToken, "_refresh")
    def test_token_expired(self, mock_refresh: MagicMock):

        self.token.expires -= 2000

        mock_refresh.return_value = "12345", 3.1415

        self.token.get("foo", "bar")

        try:
            mock_refresh.assert_called()
        except AssertionError:
            self.fail("refresh method was not called")


class TestTokenRefreshSkipped(TestCase):

    def setUp(self):
        self.token = SpotifyToken("12345", time() + 1000)

    @patch.object(SpotifyToken, "_refresh")
    def test_token_not_refreshed(self, mock_refresh: MagicMock):

        self.token.get("foo", "bar")

        try:
            mock_refresh.assert_not_called()
        except AssertionError:
            self.fail("refresh method was called")
