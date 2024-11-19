"""Module to test the active_device property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)
TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestActivePlayback(TestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    def setUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify.return_value
        }

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
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

    @patch(f"{TEST_MODULE}.Spotify")
    def setUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify.return_value
        }

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
        )

        self.account._datasets["playback_state"].expires_at = time() + 9999
        self.account._datasets["playback_state"]._data = {}

        self.result = self.account.active_device

    def test_active_device_is_expected_one(self):
        self.assertEqual(self.result, None)
