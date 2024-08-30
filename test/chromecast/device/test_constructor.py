"""Module to test the constructor of the Chromecast device class"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from custom_components.spotcast.chromecast.device import (
    ChromecastDevice,
    CastDevice,
    ChromeCastZeroconf,
    EntityNotFoundError,
    NotCastCapableError,
)

from pychromecast import Chromecast


class TestConstructionFromEntityId(TestCase):

    @patch.object(Chromecast, "wait")
    @patch.object(ChromeCastZeroconf, "get_zeroconf")
    @patch.object(ChromecastDevice, "get_hass_devices")
    def test_construction_of_device(
            self,
            mock_devices: MagicMock,
            mock_zeroconf: MagicMock,
            mock_wait: MagicMock,
    ):

        mock_hass = MagicMock()

        mock_hass.states.get.return_value.attributes.get\
            .return_value = "Mock Player"

        mock_devices.return_value = {
            "media_player.mock_player": CastDevice(
                mock_hass,
                MagicMock()
            )
        }

        device = ChromecastDevice(mock_hass, "media_player.mock_player")

        self.assertEqual(device.name, "Mock Player")
        self.assertEqual(device.entity_id, "media_player.mock_player")

        try:
            mock_wait.assert_called_once()
        except AssertionError:
            if mock_wait.call_count > 1:
                self.fail("wait method was called more than once")
            else:
                self.fail("wait method was never called")


class TestInvalidId(TestCase):

    def test_entity_id_doesnt_exist(self):

        mock_hass = MagicMock()
        mock_hass.states.get.return_value = None

        with self.assertRaises(EntityNotFoundError):
            ChromecastDevice(mock_hass, "media_player.invalid")

    @patch.object(ChromecastDevice, "get_hass_devices")
    def test_entity_id_is_not_cast_capable(self, mock_devices: MagicMock):
        mock_hass = MagicMock()
        mock_hass.states.get.return_value.attributes.get.\
            return_value = "Invalid"

        mock_devices.return_value = {
            "media_player.mock_player": "device"
        }

        with self.assertRaises(NotCastCapableError):
            ChromecastDevice(mock_hass, "media_player.invalid")
