"""Module to test the async_ensure_tokens_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
)


class TestTokenRefresh(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_external = MagicMock(spec=OAuth2Session)
        self.mock_internal = MagicMock(spec=InternalSession)

        self.account = SpotifyAccount(self.mock_external, self.mock_internal)

        await self.account.async_ensure_tokens_valid()
