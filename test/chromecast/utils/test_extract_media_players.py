"""Module to test the extract_media_players functions"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from custom_components.spotcast.chromecast.utils import (
    extract_media_players,
    CastDevice
)


class TestMediaPlayerPlatform(TestCase):

    @patch("custom_components.spotcast.chromecast.utils.EntityPlatform")
    def test_cast_device_entity(self, mock_platform: MagicMock):

        mock_platform.entities = {
            "media_player.mock_player": CastDevice(MagicMock(), MagicMock()),
        }

        results = extract_media_players(mock_platform)

        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 1)

    @patch("custom_components.spotcast.chromecast.utils.EntityPlatform")
    def test_non_cast_device_entity(self, mock_platform: MagicMock):

        mock_platform.entities = {
            "light.mock_light": MagicMock()
        }

        results = extract_media_players(mock_platform)

        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0)
