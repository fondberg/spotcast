"""Module to test the async_get_token function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)


class TestDataRetention(IsolatedAsyncioTestCase):

    @patch("custom_components.spotcast.spotify.account.Spotify")
    async def asyncSetUp(self, mock_spotify: MagicMock):

        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            mock_external,
            mock_internal,
            is_default=True
        )

        mock_internal.token = "12345"

        self.result = await self.account.async_get_token("internal")

    def test_correct_token_retrieved(self):
        self.assertEqual(self.result, "12345")
