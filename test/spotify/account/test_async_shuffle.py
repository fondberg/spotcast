"""Module to test the async_shuffle function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestSettingShuffle(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
            "hass": MagicMock(spec=HomeAssistant),
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        await self.account.async_shuffle(True, "foo")

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["public"].shuffle,
                True,
                "foo",
            )
        except AssertionError:
            self.fail()
