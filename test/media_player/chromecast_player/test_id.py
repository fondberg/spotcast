"""Module to test the id function of the chromecast_player. The id is
ment to be the MD5 hash of the device name"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from pychromecast import CastInfo

from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast,
    md5,
    ChromeCastZeroconf
)


class TestHashCalculation(TestCase):

    @patch.object(Chromecast, "name")
    def setUp(self, mock_name: MagicMock):

        mock_name.return_value = "foo"
        mock_cast_info = MagicMock(spec=CastInfo)
        mock_cast_info.cast_type = "bar"
        mock_cast_info.friendly_name = "Dummy Speaker"
        mock_cast_info.services = ["hello", "world"]
        self.device = Chromecast(
            mock_cast_info,
            zconf=MagicMock(spec=ChromeCastZeroconf)
        )

        self.expected = md5("Dummy Speaker".encode()).hexdigest()

    def test_hash_value(self):
        self.assertEqual(self.device.id, self.expected)
