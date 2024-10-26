"""Module to test the async_request function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.oauth2_session import (
    OAuth2Session,
    ConfigEntry,
    AbstractOAuth2Implementation
)

from test.unit_utils import AsyncMock


class TestRequestCall(IsolatedAsyncioTestCase):

    @patch("custom_components.spotcast.sessions.oauth2_session.async_oauth2_request")
    @patch.object(OAuth2Session, "async_ensure_token_valid", new_callable=AsyncMock)
    async def asyncSetUp(self, mock_valid: MagicMock, mock_request: MagicMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        self.mock_request = mock_request

        self.sessions = OAuth2Session(
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
