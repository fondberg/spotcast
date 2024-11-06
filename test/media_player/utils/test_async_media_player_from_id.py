"""Module to test the media_player_from_id function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
    CastDevice,
    SpotifyDevice,
    HomeAssistant,
    MediaPlayerNotFoundError,
    SpotifyAccount
)

TEST_MODULE = "custom_components.spotcast.media_player.utils"


class TestDeviceFound(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_entities_from_integration")
    async def asyncSetUp(self, mock_entities: MagicMock):

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
        mock_account = MagicMock(spec=SpotifyAccount)

        self.result = await async_media_player_from_id(
            mock_hass,
            mock_account,
            "media_player.bar"
        )

    def test_test(self):
        self.assertIs(self.result, self.mock_device)


class TestDeviceNotFound(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_entities_from_integration")
    async def test_error_raised(self, mock_entities: MagicMock):

        self.mock_device = MagicMock(spec=SpotifyDevice)

        mock_entities.side_effect = [
            {
                "media_player.foo": MagicMock(spec=CastDevice)
            },
            {}
        ]

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_account = MagicMock(spec=SpotifyAccount)

        with self.assertRaises(MediaPlayerNotFoundError):
            await async_media_player_from_id(
                mock_hass,
                mock_account,
                "media_player.bar"
            )
