"""Module to test the async_get_account"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.websocket.utils import (
    async_get_account,
    HomeAssistant,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.websocket.utils"


class TestAccountIdProvided(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_search: MagicMock,
        mock_account: AsyncMock,
        mock_entry: MagicMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "search": mock_search,
            "account": mock_account,
        }

        await async_get_account(self.mocks["hass"], "12345")

    def test_search_called(self):
        try:
            self.mocks["search"].assert_called()
        except AssertionError:
            self.fail()


class TestAccountIdNotProvided(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_search: MagicMock,
        mock_account: AsyncMock,
        mock_entry: MagicMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "search": mock_search,
            "account": mock_account,
        }

        await async_get_account(self.mocks["hass"])

    def test_async_from_config_called(self):
        try:
            self.mocks["account"].assert_called()
        except AssertionError:
            self.fail()
