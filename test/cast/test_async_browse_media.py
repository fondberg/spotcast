"""Module to test the async_browse_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.cast import (
    async_browse_media,
    HomeAssistant,
    BrowseMedia
)

TEST_MODULE = "custom_components.spotcast.cast"


class TestValidMediaType(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ha_spotify.async_browse_media")
    async def asyncSetUp(self, mock_browse: AsyncMock):

        mock_browse.return_value = MagicMock(spec=BrowseMedia)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant)
        }

        self.result = await async_browse_media(
            self.mocks["hass"],
            "spotify://",
            "spotify://12345",
            "audio"
        )

    def test_browse_media_object_returned(self):
        self.assertIsInstance(self.result, BrowseMedia)


class TestInvalidMediaType(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ha_spotify.async_browse_media")
    async def asyncSetUp(self, mock_browse: AsyncMock):

        mock_browse.return_value = MagicMock(spec=BrowseMedia)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant)
        }

        self.result = await async_browse_media(
            self.mocks["hass"],
            "plex://",
            "spotify://12345",
            "audio"
        )

    def test_none_returned(self):
        self.assertIsNone(self.result)
