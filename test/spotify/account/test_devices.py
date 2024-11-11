"""Module to test the devices property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestDevices(TestCase):

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

        self.devices = [
            {
                "id": "foo",
                "is_active": True,
                "is_private_session": False,
                "is_restricted": False,
                "name": "Dummy Chromecast",
                "type": "CastAudio",
                "volume_percent": 44,
                "supports_volume": True
            },
            {
                "id": "bar",
                "is_active": False,
                "is_private_session": False,
                "is_restricted": False,
                "name": "Web Player (Chrome)",
                "type": "Computer",
                "volume_percent": 100,
                "supports_volume": True
            }
        ]

        self.account._datasets["devices"].expires_at = time() + 999
        self.account._datasets["devices"]._data = self.devices
        self.result = self.account.devices

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, self.devices)
