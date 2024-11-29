"""Module to test the async_refresh_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ClientSession,
    ExpiredSpotifyCookiesError,
    TokenRefreshError,
    ConfigEntry,
    ContentTypeError
)


class TestSuccessfulRefresh(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get")
    async def asyncSetUp(self, mock_get: MagicMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(mock_hass, mock_entry)

        mock_get.return_value.__aenter__.return_value.headers = {}
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json\
            .return_value = await self.async_json_reply()

        self.result = await self.session.async_refresh_token()

    async def async_json_reply(self):
        return {
            "accessToken": "boo",
            "accessTokenExpirationTimestampMs": 12345.67,

        }

    async def test_valid_token_returned(self):
        self.assertEqual(self.result["access_token"], "boo")

    async def test_valid_expiration_returnd(self):
        self.assertEqual(self.result["expires_at"], 12)

    async def test_token_set_in_session(self):
        self.assertEqual(self.session._access_token, "boo")

    async def test_expiration_set_in_session(self):
        self.assertEqual(self.session._expires_at, 12)


class TestExpirationReply(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(mock_hass, mock_entry)

    async def async_json_reply(self):
        return {
            "accessToken": "boo",
            "accessTokenExpirationTimestampMs": 12345.67,

        }

    @patch.object(ClientSession, "get")
    async def test_expiration_error_raised(self, mock_get: MagicMock):
        mock_get.return_value.__aenter__.return_value.headers = {
            "Location": PrivateSession.EXPIRED_LOCATION
        }
        mock_get.return_value.__aenter__.return_value.status = 302
        mock_get.return_value.__aenter__.return_value.json\
            .return_value = await self.async_json_reply()
        with self.assertRaises(ExpiredSpotifyCookiesError):
            await self.session.async_refresh_token()


class TestClientErrors(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(mock_hass, mock_entry)

    async def async_json_reply(self):
        return {
            "accessToken": "boo",
            "accessTokenExpirationTimestampMs": 12345.67,

        }

    async def async_text_reply(self):
        return "Error Message"

    def raise_content_error(self):
        raise ContentTypeError(MagicMock(), MagicMock())

    @patch.object(ClientSession, "get")
    async def test_token_error_raised(self, mock_get: MagicMock):

        mock_get.return_value.__aenter__.return_value.headers = {
            "Location": PrivateSession.EXPIRED_LOCATION
        }
        mock_get.return_value.__aenter__.return_value.status = 403
        mock_get.return_value.__aenter__.return_value.ok = False
        mock_get.return_value.__aenter__.return_value.json\
            .return_value = await self.async_json_reply()

        with self.assertRaises(TokenRefreshError):
            await self.session.async_refresh_token()

    @patch.object(ClientSession, "get")
    async def test_none_json_answer(self, mock_get: MagicMock):

        mock_get.return_value.__aenter__.return_value.headers = {
            "Location": PrivateSession.EXPIRED_LOCATION
        }
        mock_get.return_value.__aenter__.return_value.status = 403
        mock_get.return_value.__aenter__.return_value.ok = False
        mock_get.return_value.__aenter__.return_value.json\
            .side_effect = ContentTypeError(MagicMock(), MagicMock())
        mock_get.return_value.__aenter__.return_value.text\
            .return_value = await self.async_text_reply()

        with self.assertRaises(TokenRefreshError):
            await self.session.async_refresh_token()
