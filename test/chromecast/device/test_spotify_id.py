"""Module to test the spotify_id method"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from pychromecast import Chromecast

from custom_components.spotcast.chromecast.device import (
    ChromecastDevice,
    ChromeCastZeroconf,
    CastDevice,
)


class TestSpotifyId(TestCase):

    @patch.object(Chromecast, "wait")
    @patch.object(ChromeCastZeroconf, "get_zeroconf")
    @patch.object(ChromecastDevice, "get_hass_devices")
    def setUp(
            self,
            mock_devices: MagicMock,
            mock_zeroconf: MagicMock,
            mock_wait: MagicMock,
    ):

        mock_hass = MagicMock()

        mock_hass.states.get.return_value.attributes.get\
            .return_value = "Mock Player"

        mock_cast_device = MagicMock()
        mock_cast_device.cast_info.friendly_name = "Mock Player"

        mock_devices.return_value = {
            "media_player.mock_player": CastDevice(mock_hass, mock_cast_device)
        }

        self.device = ChromecastDevice(mock_hass, "media_player.mock_player")

    def test_spotify_id_calculation(self):
        result = self.device.spotify_device_id()

        self.assertEqual(result, "b8d386889056bf2e6b7e16282c4220ed")
