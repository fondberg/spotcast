"""Module to test the async_setup_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast import (
    async_setup_entry,
    HomeAssistant,
    ConfigEntry,
    TokenRefreshError,
    ConfigEntryAuthFailed,
    InternalServerError,
    ConfigEntryNotReady,
    DOMAIN,
    MOVED_ISSUE_ID,
    MOVED_LEARN_MORE_URL,
)
from custom_components.spotcast.spotify import SpotifyAccount

TEST_MODULE = "custom_components.spotcast"


class TestEntryRegistration(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch(f"{TEST_MODULE}.async_cleanup_entities")
    @patch(f"{TEST_MODULE}.async_setup_websocket")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
        self,
        mock_account: AsyncMock,
        mock_websocket: AsyncMock,
        mock_cleanup: AsyncMock,
        mock_ir: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": mock_account.return_value,
            "entry": MagicMock(spec=ConfigEntry),
            "forward_entry": AsyncMock(),
            "register_service": MagicMock(),
            "cleanup": mock_cleanup,
        }

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["entry"].options = {
            "is_default": True,
            "base_refresh_rate": 20,
        }
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        self.mocks["cleanup"].return_value = 0

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

    def test_update_entry_not_called(self):
        try:
            self.mocks["hass"].config_entries.async_update_entry\
                .assert_not_called()
        except AssertionError:
            self.fail()


class TestDefaultOptionsSet(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch(f"{TEST_MODULE}.async_cleanup_entities")
    @patch(f"{TEST_MODULE}.async_setup_websocket")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
        self,
        mock_account: MagicMock,
        mock_websocket: AsyncMock,
        mock_cleanup: AsyncMock,
        mock_ir: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": mock_account.return_value,
            "entry": MagicMock(spec=ConfigEntry),
            "forward_entry": AsyncMock(),
            "register_service": MagicMock(),
            "cleanup": mock_cleanup,
        }

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["entry"].options = {
            "is_default": True,
        }
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        self.mocks["cleanup"].return_value = 1

        self.result = await async_setup_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_update_entry_was_called(self):
        try:
            self.mocks["hass"].config_entries.async_update_entry\
                .assert_called_with(
                    self.mocks["entry"],
                    options={
                        "is_default": True,
                        "base_refresh_rate": 30,
                    }
            )
        except AssertionError:
            self.fail()


class TestTokensErrorAtRefresh(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_token_error_raised(
        self,
        mock_account: AsyncMock,
        mock_ir: MagicMock,
    ):

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
        self.mocks["entry"].options = {}
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        with self.assertRaises(ConfigEntryAuthFailed):
            await async_setup_entry(
                self.mocks["hass"],
                self.mocks["entry"],
            )


class TestMovedIssueCreated(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch(f"{TEST_MODULE}.async_cleanup_entities")
    @patch(f"{TEST_MODULE}.async_setup_websocket")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
        self,
        mock_account: AsyncMock,
        mock_websocket: AsyncMock,
        mock_cleanup: AsyncMock,
        mock_ir: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "forward_entry": AsyncMock(),
            "ir": mock_ir,
            "cleanup": mock_cleanup,
        }

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["entry"].options = {"is_default": True}
        self.mocks["account"] = mock_account.return_value
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["cleanup"].return_value = 0

        await async_setup_entry(self.mocks["hass"], self.mocks["entry"])

    def test_moved_issue_created(self):
        self.mocks["ir"].async_create_issue.assert_called_once_with(
            self.mocks["hass"],
            DOMAIN,
            MOVED_ISSUE_ID,
            is_fixable=False,
            severity=self.mocks["ir"].IssueSeverity.WARNING,
            translation_key=MOVED_ISSUE_ID,
            learn_more_url=MOVED_LEARN_MORE_URL,
        )


class TestMovedIssueCreatedBeforeAuthFailure(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_issue_created_even_when_auth_fails(
        self,
        mock_account: AsyncMock,
        mock_ir: MagicMock,
    ):

        mock_account.side_effect = TokenRefreshError

        hass = MagicMock(spec=HomeAssistant)
        hass.data = {}
        entry = MagicMock(spec=ConfigEntry)
        entry.entry_id = "foo"
        entry.options = {}

        with self.assertRaises(ConfigEntryAuthFailed):
            await async_setup_entry(hass, entry)

        # The migration notice must reach abandoned installs that can no
        # longer authenticate, so it is created before token validation.
        mock_ir.async_create_issue.assert_called_once()


class TestGatewayError(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_token_error_raised(
        self,
        mock_account: AsyncMock,
        mock_ir: MagicMock,
    ):

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
            .side_effect = InternalServerError(503, "Dummy Error")

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "foo"
        self.mocks["entry"].options = {}
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


class TestTokensErrorAtAccountBuild(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.ir")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_token_error_raised(
        self,
        mock_account: AsyncMock,
        mock_ir: MagicMock,
    ):

        mock_account.side_effect = TokenRefreshError

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
        self.mocks["entry"].options = {}
        self.mocks["account"].is_default = True
        self.mocks["hass"].config_entries\
            .async_forward_entry_setups = self.mocks["forward_entry"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services\
            .async_register = self.mocks["register_service"]

        with self.assertRaises(ConfigEntryAuthFailed):
            await async_setup_entry(
                self.mocks["hass"],
                self.mocks["entry"],
            )
