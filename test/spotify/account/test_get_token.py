"""Module to test the get_token function"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyToken,
    SpotifyAccount,
)


class TestTokenRetrieval(TestCase):

    @patch.object(SpotifyToken, "get")
    def setUp(self, mock_get: MagicMock):
        self.account = SpotifyAccount("foo", "bar")

    @patch.object(SpotifyToken, "get")
    def test_get_token(self, mock_get: MagicMock):
        mock_get.return_value = "12345"
        self.assertEqual(self.account.get_token(), "12345")
