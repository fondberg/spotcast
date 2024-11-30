"""Module to test the async_track_features function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PrivateSession,
    PublicSession,
    HomeAssistant,
    Spotify,
)


from test.spotify.account import TEST_MODULE


RESPONSE_EXAMPLE = [
    {
        "danceability": 0.644,
        "energy": 0.714,
        "key": 1,
        "loudness": -7.696,
        "mode": 1,
        "speechiness": 0.0283,
        "acousticness": 0.0129,
        "instrumentalness": 0.02,
        "liveness": 0.11,
        "valence": 0.418,
        "tempo": 106.012,
        "type": "audio_features",
        "id": "6z7lKrdW3hwtv9hXH5YK3l",
        "uri": "spotify:track:6z7lKrdW3hwtv9hXH5YK3l",
        "track_href": ...,
        "analysis_url": ...,
        "duration_ms": 177760,
        "time_signature": 4
    }
]


class TestTrackFeature(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job\
            .return_value = RESPONSE_EXAMPLE

        self.result = await self.account.async_track_features(
            "spotify:track:foo"
        )

    def test_result_is_expected(self):
        self.assertEqual(self.result, RESPONSE_EXAMPLE[0])

    def test_properly_call_executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].audio_features,
                ["spotify:track:foo"],
            )
        except AssertionError:
            self.fail()


class TestEpisodesFeature(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job\
            .return_value = RESPONSE_EXAMPLE

        self.result = await self.account.async_track_features(
            "spotify:episode:foo"
        )

    def test_result_is_expected(self):
        self.assertEqual(self.result, {})

    def test_properly_call_executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_not_called()
        except AssertionError:
            self.fail()
