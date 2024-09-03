"""Module to test the asynchronous connect method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount, Spotify


class TestSpotifyConnection(IsolatedAsyncioTestCase):

    def setUp(self):

        mock_spotify = MagicMock(spec=Spotify)

        mock_spotify.me.return_value = {
            "display_name": "Test Account"
        }

        self.account = SpotifyAccount(mock_spotify)

    async def test_display_name_is_set(self):
        await self.account.async_connect()
        self.assertEqual(self.account.name, "Test Account")
