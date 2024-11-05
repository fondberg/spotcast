"""Module to test the unique_id property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyAccount,
    SpotifyDevice,
)


class TestValue(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
            }
        )

    def test_name_value(self):
        self.assertEqual(
            self.device.name,
            "Spotcast (Dummy User) - dummy_device",
        )
