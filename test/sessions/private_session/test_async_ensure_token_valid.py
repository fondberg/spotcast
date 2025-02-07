"""Module to test the async_ensure_token_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ConfigEntry,
    RetrySupervisor,
    UpstreamServerNotready,
    InternalServerError,
)


class TestTokenIsValid(IsolatedAsyncioTestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        self.session = PrivateSession(mock_hass, mock_entry)
        self.session._expires_at = time() + 200_000

    @patch.object(PrivateSession, "async_refresh_token")
    async def test_refresh_token_was_not_called(
            self,
            mock_refresh: MagicMock
    ):

        await self.session.async_ensure_token_valid()

        try:
            mock_refresh.assert_not_called()
        except AssertionError:
            self.fail("refresh_token was called")


class TestTokenIsNotValid(IsolatedAsyncioTestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        self.session = PrivateSession(mock_hass, mock_entry)
        self.session._expires_at = 0

    @patch.object(PrivateSession, "async_refresh_token")
    async def test_refresh_token_was_called(
            self,
            mock_refresh: AsyncMock
    ):
        await self.session.async_ensure_token_valid()

        try:
            mock_refresh.assert_called_once()
        except AssertionError:
            self.fail("refresh_token was called")


class TestUpstreamInternalServerError(IsolatedAsyncioTestCase):

    @patch.object(PrivateSession, "async_refresh_token")
    async def test_error_raised(self, mock_refresh: AsyncMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_supervisor = MagicMock(spec=RetrySupervisor)
        mock_refresh.side_effect = InternalServerError(504, "Dummy Error")

        self.session = PrivateSession(mock_hass, mock_entry)
        self.session.supervisor = mock_supervisor
        self.session.supervisor.SUPERVISED_EXCEPTIONS = RetrySupervisor\
            .SUPERVISED_EXCEPTIONS
        mock_supervisor.is_ready = True

        with self.assertRaises(UpstreamServerNotready):
            await self.session.async_ensure_token_valid()


class TestUpstreamNotReady(IsolatedAsyncioTestCase):

    async def test_error_raised(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_supervisor = MagicMock(spec=RetrySupervisor)

        self.session = PrivateSession(mock_hass, mock_entry)
        self.session.supervisor = mock_supervisor
        mock_supervisor.is_ready = False

        with self.assertRaises(UpstreamServerNotready):
            await self.session.async_ensure_token_valid()
