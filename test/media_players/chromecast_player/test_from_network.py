"""Module to test the from_network statick method"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from custom_components.spotcast.media_players.chromecast_player import (
    Chromecast,
    CastInfo,
    HostServiceInfo
)


class TestBaseDevice(TestCase):

    @patch(
        "custom_components.spotcast.media_player.chromecast_player."
        "pychromecast.get_cast_type"
    )
    def setUp(self, mock_cast_type: MagicMock):
        mock_cast_type.return_value = CastInfo(
            services={HostServiceInfo("192.168.0.10", 8009)},
            uuid=None,
            model_name=None,
            friendly_name=None,
            host="192.168.0.10",
            port=8009,
            cast_type="mock_cast",
            manufacturer="Unknown manufacturer",
        )
        self.device = Chromecast.from_network("192.168.0.10")

    def test_host_retention(self):
        self.assertEqual(self.device.cast_info.host, "192.168.0.10")

    def test_port_default(self):
        self.assertEqual(self.device.cast_info.port, 8009)

    def test_uuid_default(self):
        self.assertIsNone(self.device.uuid)

    def test_model_name_default(self):
        self.assertIsNone(self.device.model_name)

    def test_friendly_name_default(self):
        self.assertIsNone(self.device.name)

    def test_manufacturer_default(self):
        self.assertEqual(
            self.device.cast_info.manufacturer,
            "Unknown manufacturer"
        )
