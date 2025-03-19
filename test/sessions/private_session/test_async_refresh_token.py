"""Module to test the async_refresh_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
import json

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ClientSession,
    ExpiredSpotifyCookiesError,
    TokenRefreshError,
    ConfigEntry,
    ContentTypeError,
    InternalServerError,
)


class TestSuccessfulRefresh(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get", new_callable=MagicMock)
    async def asyncSetUp(self, mock_get: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "get": mock_get,
            "responses": [
                MagicMock(),
                MagicMock(),
                MagicMock(),
            ]
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        for mock_response in self.mocks["responses"]:
            mock_response.text = AsyncMock()
            mock_response.json = AsyncMock()

        self.mocks["responses"][0].json.return_value = {"serverTime": 12345}
        self.mocks["responses"][0].status = 200
        self.mocks["responses"][0].headers = {}
        self.mocks["responses"][1].text.return_value = json.dumps({
            "accessToken": "".join(["a"]*PrivateSession.TOKEN_LENGTH),
            "accessTokenExpirationTimestampMs": 123456000,
        })

        self.mocks["responses"][1].status = 200

        self.mocks["get"].return_value.__aenter__\
            .side_effect = self.mocks["responses"]

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

        self.result = await self.session.async_refresh_token()

    def test_proper_token_returned(self):
        self.assertEqual(
            self.result,
            {
                "access_token": "".join(["a"]*PrivateSession.TOKEN_LENGTH),
                "expires_at": 123456,
            }
        )


class TestUnsuccessfulRefresh(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get", new_callable=MagicMock)
    async def test_error_raised(self, mock_get: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "get": mock_get,
            "responses": [
                MagicMock(),
                MagicMock(),
            ]
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        for mock_response in self.mocks["responses"]:
            mock_response.text = AsyncMock()
            mock_response.json = AsyncMock()

        self.mocks["responses"][0].json.return_value = {"serverTime": 12345}
        self.mocks["responses"][0].status = 200
        self.mocks["responses"][0].headers = {}
        self.mocks["responses"][1].text.return_value = json.dumps({
            "_notes": "invalid",
        })

        self.mocks["responses"][1].status = 400

        for _ in range(4):
            self.mocks["responses"].append(self.mocks["responses"][1])

        self.mocks["get"].return_value.__aenter__\
            .side_effect = self.mocks["responses"]

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

        with self.assertRaises(TokenRefreshError):
            await self.session.async_refresh_token()
