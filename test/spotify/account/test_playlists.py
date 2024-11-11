"""Module to test the playlists property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestPlaylists(TestCase):

    @patch("custom_components.spotcast.spotify.account.Spotify")
    def setUp(self, mock_spotify: MagicMock):

        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            mock_external,
            mock_internal,
            is_default=True
        )

        self.playlists = [
            "foo",
            "bar"
        ]

        self.account._datasets["playlists"].expires_at = time() + 999
        self.account._datasets["playlists"]._data = self.playlists
        self.result = self.account.playlists

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, self.playlists)
