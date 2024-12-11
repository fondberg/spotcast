"""Module to test async_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.search_handler import (
    async_search_handler,
    HomeAssistant,
    ActiveConnection,
)

TEST_MODULE = "custom_components.spotcast.websocket.search_handler"


class TestBaseSearchResult(IsolatedAsyncioTestCase):
    SEARCH_RESULTS = [
        {
            "id": "1A",
            "name": "foo",
            "description": "Foo Playlists",
            "uri": "spotify:playlist:foo",
            "images": [
                {"url": "https://some.icon.jpeg", "height": 64, "width": 64},
            ],
        },
        {
            "id": "1B",
            "name": "bar",
            "href": "https://some.test2.url",
            "uri": "spotify:playlist:bar",
            "images": [
                {"url": "https://some.icon2.jpeg", "height": 64, "width": 64},
            ],
        },
        {
            "id": "1C",
            "name": "baz",
            "href": "https://some.test3.url",
            "uri": "spotify:playlist:baz",
            "images": [
                {"url": "https://some.icon3.jpeg", "height": 64, "width": 64},
            ],
        },
    ]

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_search = AsyncMock(
            return_value={"playlists": self.SEARCH_RESULTS}
        )

        self.mocks["account"].id = "12345"

        await async_search_handler(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1, "query": "foo"}
        )

    def tests_send_result_properly_called(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "playlists": [
                        {
                            "id": "1A",
                            "name": "foo",
                            "uri": "spotify:playlist:foo",
                            "description": "Foo Playlists",
                            "icon": "https://some.icon.jpeg"
                        },
                        {
                            "id": "1B",
                            "name": "bar",
                            "uri": "spotify:playlist:bar",
                            "description": None,
                            "icon": "https://some.icon2.jpeg"
                        },
                        {
                            "id": "1C",
                            "name": "baz",
                            "uri": "spotify:playlist:baz",
                            "description": None,
                            "icon": "https://some.icon3.jpeg"
                        },
                    ]
                }
            )
        except AssertionError:
            self.fail()
