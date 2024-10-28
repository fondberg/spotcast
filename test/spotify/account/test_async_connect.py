"""Module to test the async_connect function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch


from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)


class TestConnectionProcess(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_ensure_tokens_valid")
    async def asyncSetUp(self, mock_ensure: MagicMock):

        self.mock_ensure = mock_ensure

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession)
        )

        self.result = await self.account.async_connect()

    async def test_ensure_tokens_valid_called(self):
        try:
            self.mock_ensure.assert_called()
        except AssertionError:
            self.fail("ensure_tokens_valid was not called")

    async def test_function_returns_self(self):
        self.assertIs(self.result, self.account)
