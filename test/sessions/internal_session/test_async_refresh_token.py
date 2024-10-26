"""Module to test the async_refresh_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession,
    ClientSession,
    EXPIRED_LOCATION,
    ExpiredSpotifyKeyError,
    TokenError,
    ClientResponseError,
)


class TestSuccessfulRefresh(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get")
    async def asyncSetUp(self, mock_get: MagicMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")

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
        self.assertEqual(self.result[0], "boo")

    async def test_valid_expiration_returnd(self):
        self.assertEqual(self.result[1], 12)

    async def test_token_set_in_session(self):
        self.assertEqual(self.session._access_token, "boo")

    async def test_expiration_set_in_session(self):
        self.assertEqual(self.session._expires_at, 12)


class TestExpirationReply(IsolatedAsyncioTestCase):

    @patch.object(ClientSession, "get")
    async def asyncSetUp(self, mock_get: MagicMock):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")

        mock_get.return_value.__aenter__.return_value.headers = {
            "Location": EXPIRED_LOCATION
        }
        mock_get.return_value.__aenter__.return_value.status = 302
        mock_get.return_value.__aenter__.return_value.json\
            .return_value = await self.async_json_reply()

    async def async_json_reply(self):
        return {
            "accessToken": "boo",
            "accessTokenExpirationTimestampMs": 12345.67,

        }

    async def test_expiration_error_raised(self):
        with self.assertRaises(ExpiredSpotifyKeyError):
            await self.session.async_refresh_token()


class TestClientErrors(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")

    async def async_json_reply(self):
        return {
            "accessToken": "boo",
            "accessTokenExpirationTimestampMs": 12345.67,

        }

    def raise_client_error(self):
        raise ClientResponseError(MagicMock(), MagicMock())

    @patch.object(ClientSession, "get")
    async def test_token_error_raised(self, mock_get: MagicMock):

        mock_get.return_value.__aenter__.return_value.headers = {
            "Location": EXPIRED_LOCATION
        }
        mock_get.return_value.__aenter__.return_value.status = 403
        mock_get.return_value.__aenter__.return_value.ok = False
        mock_get.return_value.__aenter__.return_value.json\
            .return_value = await self.async_json_reply()

        with self.assertRaises(TokenError):
            await self.session.async_refresh_token()
