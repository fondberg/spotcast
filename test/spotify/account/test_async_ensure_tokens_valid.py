"""Module to test the async_ensure_tokens_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)


class TestTokenRefresh(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_external = MagicMock(spec=OAuth2Session)
        self.mock_internal = MagicMock(spec=InternalSession)

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            self.mock_external,
            self.mock_internal,
        )

        await self.account.async_ensure_tokens_valid()

    async def test_internal_api_called(self):
        try:
            self.mock_internal.async_ensure_token_valid.assert_called_once()
        except AssertionError:
            self.fail("Internal API token refresh was not called")

    async def test_external_api_called(self):
        try:
            self.mock_external.async_ensure_token_valid.assert_called_once()
        except AssertionError:
            self.fail("Internal API token refresh was not called")
