"""Module to test the active_device property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
)

from test.spotify.account import TEST_MODULE


class TestActivePlayback(TestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    def setUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )

        self.account._datasets["playback_state"].expires_at = time() + 9999
        self.account._datasets["playback_state"]._data = {
            "device": {
                "id": "foo"
            }
        }

        self.result = self.account.active_device

    def test_active_device_is_expected_one(self):
        self.assertEqual(self.result, "foo")


class TestNoPlayback(TestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    def setUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )

        self.account._datasets["playback_state"].expires_at = time() + 9999
        self.account._datasets["playback_state"]._data = {}

        self.result = self.account.active_device

    def test_active_device_is_expected_one(self):
        self.assertEqual(self.result, None)
