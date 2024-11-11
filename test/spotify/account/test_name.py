"""Module to test the name property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestDisplayNamePresent(TestCase):

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

        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "id": "dummy_id",
            "display_name": "Dummy Account",
        }

        self.result = self.account.name

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, "Dummy Account")


class TestDisplayNameMissing(TestCase):

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

        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "id": "dummy_id",
        }

    def test_name_is_expected_value(self):
        self.assertEqual(self.account.name, self.account.id)
