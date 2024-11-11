"""Module to test the async_repeat function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    PlaybackError,
    SpotifyException,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestSettingRepeat(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        await self.account.async_repeat(
            "context",
            "foo"
        )

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account._spotify.repeat,
                "context",
                "foo"
            )
        except AssertionError:
            self.fail()
