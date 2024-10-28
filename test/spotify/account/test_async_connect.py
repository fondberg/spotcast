"""Module to test the async_connect function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch


from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    Spotify
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestConnectionProcess(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.run_coroutine_threadsafe")
    @patch.object(Spotify, "set_auth")
    @patch.object(SpotifyAccount, "async_ensure_tokens_valid")
    async def asyncSetUp(
        self,
        mock_ensure: MagicMock,
        mock_auth: MagicMock,
        mock_coroutine: MagicMock,
    ):

        self.mock_ensure = mock_ensure
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_hass.loop = MagicMock()

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession)
        )

        mock_coroutine.return_value.result.return_value = self.account

        self.result = await self.account.async_connect()

    async def test_ensure_tokens_valid_called(self):
        try:
            self.mock_ensure.assert_called()
        except AssertionError:
            self.fail("ensure_tokens_valid was not called")

    async def test_function_returns_self(self):
        self.assertIs(self.result, self.account)
