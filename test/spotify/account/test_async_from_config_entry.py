"""Module to test the async_from_config_entry static method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    ConfigEntry,
)

TEST_MODULE = "custom_components.spotcast.spotify.account."


class TestAccountCreation(IsolatedAsyncioTestCase):

    @patch(TEST_MODULE+"async_get_config_entry_implementation")
    @patch(TEST_MODULE+"OAuth2Session", spec=OAuth2Session)
    @patch(TEST_MODULE+"InternalSession", spec=InternalSession)
    async def asyncSetUp(
            self,
            mock_external: MagicMock,
            mock_internal: MagicMock,
            mock_implementation: MagicMock,
    ):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.entry_id = "dummy_id"
        self.mock_hass.data = {
        }

        self.mock_hass.async_add_executor_job = AsyncMock(
            return_value={
                "id": "dummy",
                "display_name": "Dummy Account",
            }
        )

        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "1234",
                    "refresh_token": "5678",
                    "expires_at": 42
                },
                "implementation": "dummy_impl"
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            },
            "is_default": False,
        }

        self.account = await SpotifyAccount.async_from_config_entry(
            hass=self.mock_hass,
            entry=mock_entry,
        )

    async def test_returns_spotify_account(self):
        self.assertIsInstance(self.account, SpotifyAccount)

    async def test_account_was_added_to_hass_data(self):
        self.assertIn("spotcast", self.mock_hass.data)
        self.assertIn("dummy_id", self.mock_hass.data["spotcast"])
        self.assertIsInstance(
            self.mock_hass.data["spotcast"]["dummy_id"],
            SpotifyAccount
        )


class TestPreExistingAccount(IsolatedAsyncioTestCase):

    @patch(TEST_MODULE+"async_get_config_entry_implementation")
    @patch(TEST_MODULE+"OAuth2Session", spec=OAuth2Session)
    @patch(TEST_MODULE+"InternalSession", spec=InternalSession)
    async def asyncSetUp(
            self,
            mock_external: MagicMock,
            mock_internal: MagicMock,
            mock_implementation: MagicMock,
    ):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.entry_id = "dummy_id"
        self.mock_hass.data = {
            "spotcast": {
                "dummy_id": MagicMock(spec=SpotifyAccount)
            }
        }

        self.mock_hass.async_add_executor_job = AsyncMock(
            return_value={
                "id": "dummy",
                "display_name": "Dummy Account",
            }
        )

        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "1234",
                    "refresh_token": "5678",
                    "expires_at": 42
                },
                "implementation": "dummy_impl"
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            },
            "is_default": False,
        }

        self.account = await SpotifyAccount.async_from_config_entry(
            hass=self.mock_hass,
            entry=mock_entry,
        )

    async def test_returns_spotify_account(self):
        self.assertIsInstance(self.account, SpotifyAccount)
