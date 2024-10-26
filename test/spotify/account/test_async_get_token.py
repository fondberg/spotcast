"""Module to test the async_get_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
)


class TestInternalApi(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        mock_external = MagicMock(spec=OAuth2Session)
        mock_internal = MagicMock(spec=InternalSession)

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 1234.56
        }

        mock_internal.token = "98765"

        self.account = SpotifyAccount(mock_external, mock_internal)

        self.result = await self.account.async_get_token("internal")

    async def test_internal_token_received(self):
        self.assertEqual(self.result, "98765")


class TestInternalApi(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        mock_external = MagicMock(spec=OAuth2Session)
        mock_internal = MagicMock(spec=InternalSession)

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 1234.56
        }

        mock_internal.token = "98765"

        self.account = SpotifyAccount(mock_external, mock_internal)

        self.result = await self.account.async_get_token("external")

    async def test_internal_token_received(self):
        self.assertEqual(
            self.result,
            {"access_token": "12345", "expires_at": 1234.56}
        )
