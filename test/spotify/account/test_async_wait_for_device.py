"""Module to test the async_wait_for_device function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    TimeoutError,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestDeviceBecomingAvailable(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    async def test_return_without_error(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}
        self.account._datasets["devices"].expires_at = time() + 9999
        self.account.async_devices = AsyncMock()
        self.account.async_devices.side_effect = [
            [{"id": "foo"}],
            [{"id": "foo"}, {"id": "bar"}],
        ]

        try:
            await self.account.async_wait_for_device("bar", timeout=1)
        except TimeoutError:
            self.fail("Function raised a timeout error")


class TestDeviceNeverAvailable(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    async def test_return_without_error(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}
        self.account._datasets["devices"].expires_at = time() + 9999
        self.account.async_devices = AsyncMock()
        self.account.async_devices.return_value = [{"id": "foo"}]

        with self.assertRaises(TimeoutError):
            await self.account.async_wait_for_device("bar", timeout=1)
