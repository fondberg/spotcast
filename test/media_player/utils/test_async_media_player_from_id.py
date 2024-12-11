"""Module to test the media_player_from_id function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
    CastDevice,
    SpotifyDevice,
    HomeAssistant,
    MediaPlayerNotFoundError,
    SpotifyAccount,
    MediaPlayer,
)

TEST_MODULE = "custom_components.spotcast.media_player.utils"


class TestDeviceFound(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_entities_from_integration")
    async def asyncSetUp(self, mock_entities: AsyncMock):

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

    def test_media_player_returned(self):
        self.assertIs(self.result, self.mock_device)


class TestNoEntityId(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_active_device")
    async def asyncSetUp(self, mock_device: AsyncMock):

        mock_device.return_value = MagicMock(MediaPlayer)

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "hass": MagicMock(spec=HomeAssistant),
            "device": mock_device.return_value,
        }

        self.result = await async_media_player_from_id(
            self.mocks["hass"],
            self.mocks["account"],
        )

    def test_proper_device_returned(self):
        self.assertIs(self.result, self.mocks["device"])


class TestDeviceNotFound(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_entities_from_integration")
    async def test_error_raised(self, mock_entities: AsyncMock):

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
