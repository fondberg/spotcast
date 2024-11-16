"""Module to test async_get_playlists function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.websocket.playlists_handler import (
    async_get_playlists,
    HomeAssistant,
    ActiveConnection,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.websocket.playlists_handler"


class TestDevicesRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_entry: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_playlists = AsyncMock()
        self.mocks["account"].async_playlists.return_value = [
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
                "category": "user",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "playlists": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()


class TestAccountSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_playlists = AsyncMock()
        self.mocks["account"].async_playlists.return_value = [
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
                "category": "user"
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "playlists": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()


class TestCategoryId(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_categories = AsyncMock()
        self.mocks["account"].async_categories.return_value = [
            {
                "name": "rock",
                "id": "1234"
            }
        ]
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
                    "playlists": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()
