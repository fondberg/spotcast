"""Module to test the async_like_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Spotify,
)

from test.spotify.account import TEST_MODULE


class TestLikeSongs(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
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

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        self.account._datasets["liked_songs"].expires_at = 9999

        self.result = await self.account.async_like_media([
            "foo",
            "bar",
            "baz",
        ])

    def test_executor_properly_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].current_user_saved_tracks_add,
                ["foo", "bar", "baz"]
            )
        except AssertionError:
            self.fail()

    def test_liked_songs_dataset_set_to_expired(self):
        self.assertEqual(self.account._datasets["liked_songs"].expires_at, 0)
