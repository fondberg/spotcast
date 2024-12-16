"""Module to test the remove_device function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.device_registry import DeviceRegistry, DeviceEntry
from homeassistant.core import HomeAssistant

from custom_components.spotcast.media_player.device_manager import (
    DeviceManager,
    SpotifyAccount,
    AddEntitiesCallback
)


from test.media_player.device_manager import TEST_MODULE


class TestDeviceFound(TestCase):

    @patch(f"{TEST_MODULE}.async_get_dr")
    def setUp(self, mock_registry: MagicMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "callback": MagicMock(spec=AddEntitiesCallback),
            "registry": mock_registry.return_value,
            "device": MagicMock(spec=DeviceEntry),
        }

        self.mocks["device"].id = "foo"
        self.mocks["account"].hass = MagicMock(spec=HomeAssistant)

        self.mocks["registry"].async_get_device\
            .return_value = self.mocks["device"]

        self.manager = DeviceManager(
            self.mocks["account"],
            self.mocks["callback"],
        )

        self.manager.remove_device({("spotcast", "1234")})

    def test_get_device_properly_called(self):
        try:
            self.mocks["registry"].async_remove_device.assert_called_with(
                "foo"
            )
        except AssertionError:
            self.fail()


class TestDeviceNotFound(TestCase):

    @patch(f"{TEST_MODULE}.async_get_dr")
    def test_error_raised(self, mock_registry: MagicMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "callback": MagicMock(spec=AddEntitiesCallback),
            "registry": mock_registry.return_value,
            "device": MagicMock(spec=DeviceEntry),
        }

        self.mocks["device"].id = "foo"
        self.mocks["account"].hass = MagicMock(spec=HomeAssistant)

        self.mocks["registry"].async_get_device\
            .return_value = None

        self.manager = DeviceManager(
            self.mocks["account"],
            self.mocks["callback"],
        )

        with self.assertRaises(KeyError):
            self.manager.remove_device({("spotcast", "1234")})
