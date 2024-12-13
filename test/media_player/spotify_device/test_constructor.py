"""Module to test the constructor of the SpotifyDevice class"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice,
    SpotifyAccount,
)


class TestDataRetention(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
            }
        )

    def test_device_data_is_retained(self):
        self.assertEqual(
            self.device.device_data,
            {"id": "12345", "name": "dummy_device", "type": "dummy"},
        )

    def test_account_is_retained(self):
        self.assertIs(self.device._account, self.mock_account)

    def test_entity_id_was_created(self):
        self.assertEqual(
            self.device.entity_id,
            "media_player.dummy_device_dummy_spotcast",
        )

    def test_is_unavailable_set_to_false(self):
        self.assertFalse(self.device.is_unavailable)
