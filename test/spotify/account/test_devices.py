"""Module to test the device method"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    Spotify
)


class TestDeviceRetrieval(TestCase):

    def setUp(self):
        self.spotify = MagicMock(spec=Spotify)
        self.account = SpotifyAccount(self.spotify)

    def test_device_read(self):

        self.spotify.devices.return_value = {
            "devices": [
                {
                    "name": "Mock_1",
                    "id": "12345"
                },
                {
                    "name": "Mock_2",
                    "id": "23456"
                }
            ]
        }

        result = self.account.devices()

        self.assertEqual(len(result), 2)
