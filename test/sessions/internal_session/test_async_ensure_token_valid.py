"""Module to test the async_ensure_token_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from time import time

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession,
    ConfigEntry
)


class TestTokenIsValid(IsolatedAsyncioTestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        self.session = InternalSession(mock_hass, mock_entry)
        self.session._expires_at = time() + 200_000

    @patch.object(InternalSession, "async_refresh_token")
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

        self.session = InternalSession(mock_hass, mock_entry)
        self.session._expires_at = 0

    @patch.object(InternalSession, "async_refresh_token")
    async def test_refresh_token_was_called(
            self,
            mock_refresh: MagicMock
    ):
        await self.session.async_ensure_token_valid()

        try:
            mock_refresh.assert_called_once()
        except AssertionError:
            self.fail("refresh_token was called")
