"""Module to test the constructor of the spotify account class"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    SpotifyToken,
)


class TestDataRetention(TestCase):

    @patch.object(SpotifyToken, "get")
    def setUp(self, mock_get: MagicMock):
        mock_get.return_value = "12345"
        self.account = SpotifyAccount("foo", "bar", "CA")

    def test_sp_dc_retention(self):
        self.assertEqual(self.account._sp_dc, "foo")

    def test_sp_key_retention(self):
        self.assertEqual(self.account._sp_key, "bar")
