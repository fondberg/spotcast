"""Module to test the async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)


class TestMediaCasting(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.mock_hass.async_add_executor_job = AsyncMock()

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        await self.account.async_play_media("foo", "uri")

    async def test_start_playback_called_in_executor_loop(self):
        try:
            self.mock_hass.async_add_executor_job.assert_called_with(
                self.account._spotify.start_playback,
                "foo",
                "uri",
            )
        except AssertionError:
            self.fail()
