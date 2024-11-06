"""Module to test the async_setup_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast import (
    async_setup_entry,
    HomeAssistant,
    SpotifyAccount,
    SERVICE_SCHEMAS,
    ConfigEntry,
    TokenRefreshError,
    ConfigEntryNotReady,
)


class TestEntryRegistration(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry", new_callable=AsyncMock)
    async def asyncSetUp(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": mock_account.return_value,
            "entry": MagicMock(spec=ConfigEntry),
            "forward_entry": AsyncMock(),
            "register_service": MagicMock(),
        }

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        self.result = await async_setup_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_function_returns_true(self):
        self.assertTrue(self.result)

    def test_service_were_registered(self):
        try:
            self.mocks["register_service"].assert_called()
        except AssertionError:
            self.fail()


class TestTokensError(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry", new_callable=AsyncMock)
    async def test_token_error_raised(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": mock_account.return_value,
            "entry": MagicMock(spec=ConfigEntry),
            "forward_entry": AsyncMock(),
            "register_service": MagicMock(),
        }

        self.mocks["account"].async_ensure_tokens_valid = AsyncMock()
        self.mocks["account"].async_ensure_tokens_valid\
            .side_effect = TokenRefreshError

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        with self.assertRaises(ConfigEntryNotReady):
            await async_setup_entry(
                self.mocks["hass"],
                self.mocks["entry"],
            )
