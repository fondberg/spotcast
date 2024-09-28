"""Module to test the connect method"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount, Spotify


class TestSpotifyConnection(TestCase):

    def setUp(self):

        mock_spotify = MagicMock(spec=Spotify)

        mock_spotify.me.return_value = {
            "display_name": "Test Account"
        }

        self.account = SpotifyAccount(mock_spotify)

    def test_display_name_is_set(self):
        self.account.connect()
        self.assertEqual(self.account.name, "Test Account")
