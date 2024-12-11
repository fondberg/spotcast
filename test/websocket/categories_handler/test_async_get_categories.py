"""Module to test the async_get_devices function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.categories_handler import (
    async_get_categories,
    HomeAssistant,
    ActiveConnection,
)

TEST_MODULE = "custom_components.spotcast.websocket.categories_handler"
CATEGORIES = [
    {
        "href": (
            "https://api.spotify.com/v1/browse/categories/"
            "foo"
        ),
        "id": "foo",
        "icons": [
            {
                "height": 274,
                "url": "https://t.scdn.co/images/foo.jpeg",
                "width": 274
            }
        ],
        "name": "Made For You"
    },
    {
        "href": "https://api.spotify.com/v1/browse/categories/bar",
        "id": "bar",
        "icons": [
            {
                "height": 274,
                "url": "https://t.scdn.co/images/bar.jpeg",
                "width": 274
            }
        ],
        "name": "Discover"
    },
    {
        "href": "https://api.spotify.com/v1/browse/categories/baz",
        "id": "baz",
        "icons": [
            {
                "height": 274,
                "url": "https://t.scdn.co/images/baz.jpeg",
                "width": 274
            }
        ],
        "name": "Metal"
    },
]


class TestDevicesRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].id = "12345"
        self.mocks["account"].async_categories = AsyncMock(
            return_value=CATEGORIES
        )

        await async_get_categories(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/categories",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "categories": [
                        {
                            "id": "foo",
                            "icon": "https://t.scdn.co/images/foo.jpeg",
                            "name": "Made For You"
                        },
                        {
                            "id": "bar",
                            "icon": "https://t.scdn.co/images/bar.jpeg",
                            "name": "Discover"
                        },
                        {
                            "id": "baz",
                            "icon": "https://t.scdn.co/images/baz.jpeg",
                            "name": "Metal"
                        },
                    ]
                }
            )
        except AssertionError:
            self.fail()
