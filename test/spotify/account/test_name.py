"""Module to test the name property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Spotify,
)

from test.spotify.account import TEST_MODULE


class TestDisplayNamePresent(TestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    def setUp(self, mock_spotify: MagicMock):

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

        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "id": "dummy_id",
            "display_name": "Dummy Account",
        }

        self.result = self.account.name

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, "Dummy Account")


class TestDisplayNameMissing(TestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    def setUp(self, mock_spotify: MagicMock):

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

        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "id": "dummy_id",
        }

    def test_name_is_expected_value(self):
        self.assertEqual(self.account.name, self.account.id)
