"""Module to test the media_player_from_id function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.utils import (
    media_player_from_id,
    CastDevice,
    SpotifyDevice,
    HomeAssistant,
    MediaPlayerNotFoundError,
)

TEST_MODULE = "custom_components.spotcast.media_player.utils"


class TestDeviceFound(TestCase):

    @patch(f"{TEST_MODULE}.entities_from_integration")
    def setUp(self, mock_entities: MagicMock):

        self.mock_device = MagicMock(spec=SpotifyDevice)

        mock_entities.side_effect = [
            {
                "media_player.foo": MagicMock(spec=CastDevice)
            },
            {
                "media_player.bar": self.mock_device
            },
        ]

        mock_hass = MagicMock(spec=HomeAssistant)

        self.result = media_player_from_id(mock_hass, "media_player.bar")

    def test_test(self):
        self.assertIs(self.result, self.mock_device)


class TestDeviceNotFound(TestCase):

    @patch(f"{TEST_MODULE}.entities_from_integration")
    def test_error_raised(self, mock_entities: MagicMock):

        self.mock_device = MagicMock(spec=SpotifyDevice)

        mock_entities.side_effect = [
            {
                "media_player.foo": MagicMock(spec=CastDevice)
            },
            {}
        ]

        mock_hass = MagicMock(spec=HomeAssistant)

        with self.assertRaises(MediaPlayerNotFoundError):
            media_player_from_id(mock_hass, "media_player.bar")
