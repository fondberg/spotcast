"""Module to test the id function of the chromecast_player. The id is
ment to be the MD5 hash of the device name"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from pychromecast import CastInfo, HostServiceInfo

from custom_components.spotcast.media_players.chromecast_player import (
    Chromecast,
    md5
)


class TestHashCalculation(TestCase):
    @patch(
        "custom_components.spotcast.media_players.chromecast_player."
        "pychromecast.get_cast_type"
    )
    def setUp(self, mock_cast_type: MagicMock):
        mock_cast_type.return_value = CastInfo(
            services={HostServiceInfo("192.168.0.10", 8009)},
            uuid=None,
            model_name=None,
            friendly_name="Mock Player",
            host="192.168.0.10",
            port=8009,
            cast_type="mock_cast",
            manufacturer="Unknown manufacturer",
        )
        self.device = Chromecast.from_network("192.168.0.10")

    def test_hash_value(self):
        expected = md5("Mock Player".encode()).hexdigest()

        self.assertEqual(expected, self.device.id)
