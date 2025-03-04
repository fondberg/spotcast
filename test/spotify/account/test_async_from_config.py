"""Module to test the async_from_config_entry static method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    ConfigEntry,
    PublicSession,
    PrivateSession,
    Store,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestAccountCreationWithoutDomainData(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(PrivateSession, "async_ensure_token_valid")
    @patch.object(PublicSession, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
        mock_store: MagicMock,
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

    def test_entry_id_saved_on_account(self):
        self.assertEqual(self.result.entry_id, "12345")


class TestAccountCreationWithDomainData(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(PrivateSession, "async_ensure_token_valid")
    @patch.object(PublicSession, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
        mock_store: MagicMock,
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

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_profile")
    @patch.object(PrivateSession, "async_ensure_token_valid")
    @patch.object(PublicSession, "async_ensure_token_valid")
    @patch(f"{TEST_MODULE}.async_get_config_entry_implementation")
    async def asyncSetUp(
        self,
        mock_implementation: AsyncMock,
        mock_ensure_external: AsyncMock,
        mock_ensure_internal: AsyncMock,
        mock_profile: AsyncMock,
        mock_store: MagicMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "implementation": mock_implementation.return_value,
        }

        self.mocks["hass"].data = {"spotcast": {
            "12345": {
                "account": SpotifyAccount(
                    entry_id="12345",
                    hass=self.mocks["hass"],
                    public_session=MagicMock(spec=PublicSession),
                    private_session=MagicMock(spec=PrivateSession),
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
