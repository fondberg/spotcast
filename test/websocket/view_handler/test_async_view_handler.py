"""Module to test the async_view_handler function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.view_handler import (
    async_view_handler,
    HomeAssistant,
    ActiveConnection,
)

TEST_MODULE = "custom_components.spotcast.websocket.view_handler"


class TestViewQuery(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].id = "12345"
        self.mocks["account"].async_view = AsyncMock(return_value=[
            {
                "id": "foo",
                "name": "Foo",
                "uri": "spotify:playlist:foo",
                "description": "Playlist Foo",
                "images": [
                    {
                        "url": "https://some.icon1.jpeg",
                        "height": 64,
                        "width": 64,
                    }
                ]
            },
            {
                "id": "bar",
                "name": "Bar",
                "uri": "spotify:playlist:bar",
                "description": "Playlist Bar",
                "images": [
                    {
                        "url": "https://some.icon2.jpeg",
                        "height": 64,
                        "width": 64,
                    }
                ]
            },
            {
                "id": "baz",
                "name": "Baz",
                "uri": "spotify:playlist:baz",
                "description": "Playlist Baz",
                "images": [
                    {
                        "url": "https://some.icon3.jpeg",
                        "height": 64,
                        "width": 64,
                    }
                ]
            },
        ])

        await async_view_handler(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/view",
                "name": "made-for-x",
            }
        )

    def test_async_view_properly_called(self):
        try:
            self.mocks["account"].async_view.assert_called_with(
                url="views/made-for-x",
                language=None,
                limit=None,
            )
        except AssertionError:
            self.fail()

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "playlists": [
                        {
                            "id": "foo",
                            "name": "Foo",
                            "uri": "spotify:playlist:foo",
                            "description": "Playlist Foo",
                            "icon": "https://some.icon1.jpeg"
                        },
                        {
                            "id": "bar",
                            "name": "Bar",
                            "uri": "spotify:playlist:bar",
                            "description": "Playlist Bar",
                            "icon": "https://some.icon2.jpeg"
                        },
                        {
                            "id": "baz",
                            "name": "Baz",
                            "uri": "spotify:playlist:baz",
                            "description": "Playlist Baz",
                            "icon": "https://some.icon3.jpeg"
                        },
                    ]
                }
            )
        except AssertionError:
            self.fail()
