"""Module to test the chromecast_player from hass constructor"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from zeroconf import Zeroconf

from custom_components.spotcast.media_players.chromecast_player import (
    Chromecast,
    CastInfo,
    HostServiceInfo,
    MediaPlayerNotFoundError,
    ChromeCastZeroconf
)


class TestIntegratedMediaPlayer(TestCase):

    @patch.object(ChromeCastZeroconf, "get_zeroconf")
    @patch.object(Chromecast, "_get_entities_from_platforms")
    def test_device_found_in_hass(
            self,
            mock_entities: MagicMock,
            mock_zeroconf: MagicMock
    ):
        mock_zeroconf.return_value = MagicMock(spec=Zeroconf)
        mock_device = MagicMock()

        mock_device._cast_info.cast_info = CastInfo(
            services={HostServiceInfo("192.168.0.10", 8009)},
            uuid=None,
            model_name=None,
            friendly_name="Mock Player",
            host="192.168.0.10",
            port=8009,
            cast_type="mock",
            manufacturer=None,
        )

        mock_entities.return_value = {
            "media_player.mock_player": mock_device
        }

        mock_hass = MagicMock()

        result = Chromecast.from_hass(
            mock_hass, "media_player.mock_player")

        self.assertEqual(result.name, "Mock Player")


class TestMissingMediaPlayer(TestCase):

    @patch.object(Chromecast, "_get_entities_from_platforms")
    def test_device_not_found_in_hass(self, mock_entities: MagicMock):

        mock_entities.return_value = {}

        with self.assertRaises(MediaPlayerNotFoundError):
            Chromecast.from_hass(MagicMock(), "media_player.mock_player")
