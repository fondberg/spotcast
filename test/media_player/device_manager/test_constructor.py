"""Module to test the constructor of the DeviceManager"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.media_player.device_manager import (
    DeviceManager,
    SpotifyAccount,
    AddEntitiesCallback
)


class TestDataRetention(TestCase):

    def setUp(self):

        self.mock_callback = MagicMock(spec=AddEntitiesCallback)
        self.mock_account = MagicMock(spec=SpotifyAccount)

        self.device_manager = DeviceManager(
            self.mock_account,
            self.mock_callback,
        )

    def test_tracked_devices_initialized(self):
        self.assertEqual(self.device_manager.tracked_devices, {})

    def test_account_retained(self):
        self.assertEqual(self.device_manager._account, self.mock_account)

    def test_callback_retained(self):
        self.assertEqual(
            self.device_manager.async_add_entities,
            self.mock_callback,
        )
