"""Module to test async_ensure_token_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time
from aiohttp.client_exceptions import ClientConnectorDNSError

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor,
)
from custom_components.spotcast.sessions.public_session import (
    PublicSession,
    ConfigEntry,
    AbstractOAuth2Implementation,
    TokenRefreshError,
    ClientResponseError,
    UpstreamServerNotready,
)


class TestTokenIsValid(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo",
                    "expires_at": time() + 200_000,

                }
            }
        }

        self.session = PublicSession(
            hass=self.mock_hass,
            entry=mock_entry,
            implementation=self.mock_implementation
        )

        await self.session.async_ensure_token_valid()

    async def test_async_refresh_token_not_called(self):
        try:
            self.mock_implementation.async_refresh_token.assert_not_called()
        except AssertionError:
            self.fail("Refresh Token was called")

    async def test_update_entry_not_called(self):
        try:
            self.mock_hass.config_entries.async_update_entry\
                .assert_not_called()
        except AssertionError:
            self.fail("Update Entry was called")


class TestTokenIsNotValid(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo",
                    "expires_at": 0,

                }
            }
        }

        self.session = PublicSession(
            hass=self.mock_hass,
            entry=mock_entry,
            implementation=self.mock_implementation
        )

        await self.session.async_ensure_token_valid()

    async def test_async_refresh_token_not_called(self):
        try:
            self.mock_implementation.async_refresh_token.assert_called()
        except AssertionError:
            self.fail("Refresh Token was not called")

    async def test_update_entry_not_called(self):
        try:
            self.mock_hass.config_entries.async_update_entry.assert_called()
        except AssertionError:
            self.fail("Update Entry was not called")


class TestTokenFailsToRefresh(IsolatedAsyncioTestCase):

    async def test_raises_appropriate_error(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo",
                    "expires_at": 0,

                }
            }
        }

        self.mock_implementation.async_refresh_token = AsyncMock()
        self.mock_implementation.async_refresh_token\
            .side_effect = ClientResponseError(MagicMock(), MagicMock())

        self.session = PublicSession(
            hass=self.mock_hass,
            entry=mock_entry,
            implementation=self.mock_implementation
        )

        with self.assertRaises(TokenRefreshError):
            await self.session.async_ensure_token_valid()


class TestNetworkIssues(IsolatedAsyncioTestCase):

    async def test_raises_appropriate_error(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo",
                    "expires_at": 0,

                }
            }
        }

        self.mock_implementation.async_refresh_token = AsyncMock()
        self.mock_implementation.async_refresh_token\
            .side_effect = ClientConnectorDNSError(MagicMock(), MagicMock())

        self.session = PublicSession(
            hass=self.mock_hass,
            entry=mock_entry,
            implementation=self.mock_implementation
        )

        with self.assertRaises(UpstreamServerNotready):
            await self.session.async_ensure_token_valid()


class TestSupervisorNotReady(IsolatedAsyncioTestCase):

    async def test_raises_appropriate_error(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_retry = MagicMock(spec=RetrySupervisor)
        self.mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo",
                    "expires_at": 0,

                }
            }
        }

        self.mock_implementation.async_refresh_token = AsyncMock()
        self.mock_implementation.async_refresh_token\
            .side_effect = ClientConnectorDNSError(MagicMock(), MagicMock())

        self.session = PublicSession(
            hass=self.mock_hass,
            entry=mock_entry,
            implementation=self.mock_implementation
        )
        self.session.supervisor = self.mock_retry
        self.session.supervisor.SUPERVISED_EXCEPTIONS = RetrySupervisor\
            .SUPERVISED_EXCEPTIONS
        self.session.supervisor.is_ready = False

        with self.assertRaises(UpstreamServerNotready):
            await self.session.async_ensure_token_valid()
