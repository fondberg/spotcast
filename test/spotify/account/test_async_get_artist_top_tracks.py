"""Module to test the async_get_album function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PrivateSession,
    PublicSession,
    HomeAssistant,
    Spotify,
)

from test.spotify.account import TEST_MODULE

API_RESULT = {
    "tracks": [
        "foo",
        "bar",
        "baz",
    ]
}


class TestPlayslistRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.return_value = API_RESULT

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            private_session=self.mocks["internal"],
            public_session=self.mocks["external"],
        )

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.result = await self.account.async_get_artist_top_tracks(
            "spotify:artist:foo"
        )

    def test_proper_result_returned(self):
        self.assertEqual(API_RESULT["tracks"], self.result)

    def test_proper_call_to__executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].artist_top_tracks,
                "spotify:artist:foo",
                "CA",
            )
        except AssertionError:
            self.fail()
