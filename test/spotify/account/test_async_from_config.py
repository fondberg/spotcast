"""Module to test the async_from_config_entry static method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    ConfigEntry,
    OAuth2Session,
    InternalSession,
    ConfigEntry,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestAccountCreationWithoutDomainData(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(InternalSession, "async_ensure_token_valid")
    @patch.object(OAuth2Session, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "implementation": mock_implementation.return_value,
        }

        self.mocks["hass"].data = {}
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].data = {
            "external_api": {
                "token": {
                    "access_token": "foo",
                    "refresh_token": "bar",
                    "expires_at": 0,
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            }
        }
        self.mocks["entry"].options = {
            "is_default": True,
            "base_refresh_rate": 30,
        }

        self.result = await SpotifyAccount.async_from_config_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_result_is_spotify_account(self):
        self.assertIsInstance(self.result, SpotifyAccount)


class TestAccountCreationWithDomainData(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(InternalSession, "async_ensure_token_valid")
    @patch.object(OAuth2Session, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "implementation": mock_implementation.return_value,
        }

        self.mocks["hass"].data = {"spotcast": {}}
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].data = {
            "external_api": {
                "token": {
                    "access_token": "foo",
                    "refresh_token": "bar",
                    "expires_at": 0,
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            }
        }
        self.mocks["entry"].options = {
            "is_default": True,
            "base_refresh_rate": 30,
        }

        self.result = await SpotifyAccount.async_from_config_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_result_is_spotify_account(self):
        self.assertIsInstance(self.result, SpotifyAccount)


class TestPreexistingAccount(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(InternalSession, "async_ensure_token_valid")
    @patch.object(OAuth2Session, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "implementation": mock_implementation.return_value,
        }

        self.mocks["hass"].data = {"spotcast": {
            "12345": {
                "account": SpotifyAccount(
                    self.mocks["hass"],
                    MagicMock(spec=OAuth2Session),
                    MagicMock(spec=InternalSession),
                    is_default=True,
                )
            }
        }}
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].data = {
            "external_api": {
                "token": {
                    "access_token": "foo",
                    "refresh_token": "bar",
                    "expires_at": 0,
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            }
        }
        self.mocks["entry"].options = {
            "is_default": True,
            "base_refresh_rate": 30,
        }

        self.result = await SpotifyAccount.async_from_config_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_result_is_spotify_account(self):
        self.assertIsInstance(self.result, SpotifyAccount)
