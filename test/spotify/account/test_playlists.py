"""Module to test the playlists property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestPlaylists(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    def setUp(self, mock_spotify: MagicMock, mock_store: MagicMock):

        mock_internal = MagicMock(spec=PrivateSession)
        mock_external = MagicMock(spec=PublicSession)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=MagicMock(spec=HomeAssistant),
            public_session=mock_external,
            private_session=mock_internal,
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
