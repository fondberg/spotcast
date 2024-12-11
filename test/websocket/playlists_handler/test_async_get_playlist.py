"""Module to test async_get_playlists function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.playlists_handler import (
    async_get_playlists,
    HomeAssistant,
    ActiveConnection,
)

TEST_MODULE = "custom_components.spotcast.websocket.playlists_handler"


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
        self.mocks["account"].async_playlists = AsyncMock(return_value=[
            "foo",
            "bar",
            "baz",
        ])

        await async_get_playlists(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/devices",
                "category": "user",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "category": "user",
                    "playlists": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()


class TestCategoryId(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].id = "12345"
        self.mocks["account"].async_categories = AsyncMock(return_value=[
            {
                "name": "rock",
                "id": "1234"
            }
        ])
        self.mocks["account"].async_category_playlists = AsyncMock()
        self.mocks["account"].async_category_playlists.return_value = [
            "foo",
            "bar",
            "baz",
        ]

        await async_get_playlists(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/devices",
                "account": "12345",
                "category": "rock"
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "category": "1234",
                    "playlists": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()
