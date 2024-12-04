"""Module to test the async_request function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.public_session import (
    PublicSession,
    ConfigEntry,
    OAuth2Session,
)

from test.sessions.public_session import TEST_MODULE


class TestRequestCall(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_oauth2_request")
    @patch.object(PublicSession, "async_ensure_token_valid")
    async def asyncSetUp(self, mock_valid: AsyncMock, mock_request: AsyncMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_implementation = MagicMock(spec=OAuth2Session)
        self.mock_request = mock_request

        self.sessions = PublicSession(
            mock_hass,
            mock_entry,
            mock_implementation
        )

        self.sessions.config_entry.data = {
            "external_api": {
                "token": "boo"
            }
        }

        await self.sessions.async_request("GET", "http://localhost/test")

    async def test_request_properly_called(self):
        try:
            self.mock_request.assert_called_with(
                self.sessions.hass,
                "boo",
                "GET",
                "http://localhost/test"
            )
        except AssertionError:
            self.fail()
