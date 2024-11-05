"""Module ot test the define_entity_id function for the SpoitfyDevice
class"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyAccount,
    SpotifyDevice,
)


class TestSimpleName(TestCase):

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
                "is_active": True,
            }
        )

    def test_simple_name(self):
        self.assertEqual(
            self.device._define_entity_id(),
            "media_player.dummy_device_dummy_spotcast"
        )


class TestComplexName(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "Dummy Device (Chrome)",
                "type": "dummy",
                "is_active": True,
            }
        )

    def test_simple_name(self):
        self.assertEqual(
            self.device._define_entity_id(),
            "media_player.dummy_device_chrome_dummy_spotcast"
        )
