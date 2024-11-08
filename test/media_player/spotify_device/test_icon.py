"""Module to test the icon property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice,
    SpotifyAccount,
)


class TestComputerDevice(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.device = SpotifyDevice(
            self.mocks["account"],
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "Computer",
                "is_active": True,
            }
        )

    def test_device_active(self):
        self.assertEqual(self.device.icon, "mdi:laptop")

    def test_device_inactive(self):
        self.device._device_data["is_active"] = False
        self.assertEqual(self.device.icon, "mdi:laptop-off")

    def test_device_unavailable(self):
        self.device._is_unavailable = True
        self.assertEqual(self.device.icon, "mdi:laptop")


class TestSmartphoneDevice(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.device = SpotifyDevice(
            self.mocks["account"],
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "Smartphone",
                "is_active": True,
            }
        )

    def test_device_active(self):
        self.assertEqual(self.device.icon, "mdi:smartphone")

    def test_device_inactive(self):
        self.device._device_data["is_active"] = False
        self.assertEqual(self.device.icon, "mdi:smartphone-off")

    def test_device_unavailable(self):
        self.device._is_unavailable = True
        self.assertEqual(self.device.icon, "mdi:smartphone")


class TestUnknownDevice(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.device = SpotifyDevice(
            self.mocks["account"],
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "Dummy",
                "is_active": True,
            }
        )

    def test_device_active(self):
        self.assertEqual(self.device.icon, "mdi:speaker")

    def test_device_inactive(self):
        self.device._device_data["is_active"] = False
        self.assertEqual(self.device.icon, "mdi:speaker-off")

    def test_device_unavailable(self):
        self.device._is_unavailable = True
        self.assertEqual(self.device.icon, "mdi:speaker")
