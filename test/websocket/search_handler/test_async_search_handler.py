"""Module to test async_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.websocket.search_handler import (
    async_search_handler,
    HomeAssistant,
    ActiveConnection,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.websocket.search_handler"

class TestSearchHandler(IsolatedAsyncioTestCase):
    SEARCH_RESULTS = [
        {
            "id": "1A",
            "name": "foo",
            "href": "https://some.test.url",
            "images": [{"url": "https://some.icon.jpeg"}],
        },
        {
            "id": "1B",
            "name": "bar",
            "href": "https://some.test2.url",
            "images": [{"url": "https://some.icon2.jpeg"}],
        },
        {
            "id": "1C",
            "name": "BAZ",
            "href": "https://some.test3.url",
            "images": [{"url": "https://some.icon3.jpeg"}],
        },
    ]

    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_search_account: MagicMock):
        """Set up mocks for async_search_handler tests."""

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_search_account.return_value = mock_account.return_value

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_search = AsyncMock()
        self.mocks["account"].async_search.return_value = {"playlists": self.SEARCH_RESULTS}

    async def test_playlist_search(self):
        """Test search handler for playlists."""
        await async_search_handler(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/search",
                "query": "my query",
                "searchType": "playlist",
                "limit": 3,
                "account": "12345",
            },
        )

        self.mocks["connection"].send_result.assert_called_with(
            1,
            {
                "total": 3,
                "account": "12345",
                "playlists": [
                    {
                        "id": "1A",
                        "name": "foo",
                        "href": "https://some.test.url",
                        "icon": "https://some.icon.jpeg",
                    },
                    {
                        "id": "1B",
                        "name": "bar",
                        "href": "https://some.test2.url",
                        "icon": "https://some.icon2.jpeg",
                    },
                    {
                        "id": "1C",
                        "name": "BAZ",
                        "href": "https://some.test3.url",
                        "icon": "https://some.icon3.jpeg",
                    },
                ],
            },
        )

    async def test_track_search(self):
        """Test search handler for tracks."""
        self.mocks["account"].async_search.return_value = {
            "tracks": self.SEARCH_RESULTS
        }

        await async_search_handler(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 2,
                "type": "spotcast/search",
                "query": "another query",
                "searchType": "track",
                "limit": 3,
                "account": "12345",
            },
        )

        self.mocks["connection"].send_result.assert_called_with(
            2,
            {
                "total": 3,
                "account": "12345",
                "tracks": [
                    {
                        "id": "1A",
                        "name": "foo",
                        "href": "https://some.test.url",
                        "icon": "https://some.icon.jpeg",
                    },
                    {
                        "id": "1B",
                        "name": "bar",
                        "href": "https://some.test2.url",
                        "icon": "https://some.icon2.jpeg",
                    },
                    {
                        "id": "1C",
                        "name": "BAZ",
                        "href": "https://some.test3.url",
                        "icon": "https://some.icon3.jpeg",
                    },
                ],
            },
        )
