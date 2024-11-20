"""Module to test the async_get_media_browser_root_object"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.cast import (
    async_get_media_browser_root_object,
    HomeAssistant,
    BrowseMedia
)

TEST_MODULE = "custom_components.spotcast.cast"


class TestBrowseMediaRetreival(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ha_spotify.async_browse_media")
    async def asyncSetUp(self, mock_browse: AsyncMock):

        mock_browse.return_value = MagicMock(spec=BrowseMedia)
        mock_browse.return_value.children = [
            MagicMock(spec=BrowseMedia),
            MagicMock(spec=BrowseMedia),
            MagicMock(spec=BrowseMedia),
        ]

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant)
        }

        self.result = await async_get_media_browser_root_object(
            self.mocks["hass"],
            "audio"
        )

    def test_received_list_of_media_browser(self):
        self.assertIsInstance(self.result, list)

        for item in self.result:
            self.assertIsInstance(item, BrowseMedia)
