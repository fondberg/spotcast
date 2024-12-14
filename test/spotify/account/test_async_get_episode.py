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
    "audio_preview_url": ...,
    "description": ...,
    "html_description": ...,
    "duration_ms": 5079719,
    "explicit": False,
    "external_urls": {
        "spotify": "https://open.spotify.com/episode/4Nrn0IIzH1DJzxGN3rniox"
    },
    "href": "https://api.spotify.com/v1/episodes/4Nrn0IIzH1DJzxGN3rniox",
    "id": "4Nrn0IIzH1DJzxGN3rniox",
    "images": [
        {
            "url": ...,
            "height": 640,
            "width": 640
        },
        {
            "url": ...,
            "height": 300,
            "width": 300
        },
        {
            "url": ...,
            "height": 64,
            "width": 64
        }
    ],
    "is_externally_hosted": False,
    "is_playable": True,
    "language": "en",
    "languages": [
        "en"
    ],
    "name": "C03 - Ep. 05 - Mission Through Middrus - Mined like a Steal Trap",
    "release_date": "2024-11-27",
    "release_date_precision": "day",
    "resume_point": {
        "fully_played": True,
        "resume_position_ms": 0
    },
    "type": "episode",
    "uri": "spotify:episode:4Nrn0IIzH1DJzxGN3rniox",
    "show": {
        "copyrights": [],
        "description": ...,
        "html_description": ...,
        "explicit": False,
        "external_urls": {
            "spotify": "https://open.spotify.com/show/1QQJ7FElLE0K6CIfZNCxU4"
        },
        "href": "https://api.spotify.com/v1/shows/1QQJ7FElLE0K6CIfZNCxU4",
        "id": "1QQJ7FElLE0K6CIfZNCxU4",
        "images": [
            {
                "url": ...,
                "height": 640,
                "width": 640
            },
            {
                "url": ...,
                "height": 300,
                "width": 300
            },
            {
                "url": ...,
                "height": 64,
                "width": 64
            }
        ],
        "is_externally_hosted": False,
        "languages": ["en"],
        "media_type": "audio",
        "name": "Tales from the Stinky Dragon",
        "publisher": "Stinky Dragon",
        "type": "show",
        "uri": "spotify:show:1QQJ7FElLE0K6CIfZNCxU4",
        "total_episodes": 174
    }
}


class TestEpisodeRetrieval(IsolatedAsyncioTestCase):

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

        self.result = await self.account.async_get_episode(
            "spotify:episode:foo"
        )

    def test_proper_result_returned(self):
        self.assertEqual(API_RESULT, self.result)

    def test_proper_call_to_executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].episode,
                "spotify:episode:foo",
                "CA",
            )
        except AssertionError:
            self.fail()
