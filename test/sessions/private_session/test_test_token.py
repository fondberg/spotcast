"""Module to test the test_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    HomeAssistant,
    ConfigEntry,
    TokenRefreshError,
    ClientSession,
)


class TestValidToken(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get", new_callable=MagicMock)
    async def test_no_error_raised(self, mock_get: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "get": mock_get,
            "response": mock_get.return_value.__aenter__.return_value
        }

        self.mocks["response"].json = AsyncMock()
        self.mocks["response"].json.return_value = {"foo": "bar"}
        self.mocks["response"].ok = True

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

        try:
            await self.session._test_token("foo")
        except TokenRefreshError as exc:
            self.fail(exc)


class TestInvalidToken(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get", new_callable=MagicMock)
    async def test_error_raised(self, mock_get: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "get": mock_get,
            "response": mock_get.return_value.__aenter__.return_value
        }

        self.mocks["response"].json = AsyncMock()
        self.mocks["response"].json.return_value = {"foo": "bar"}
        self.mocks["response"].ok = False

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar"
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

        with self.assertRaises(TokenRefreshError):
            await self.session._test_token("foo")
