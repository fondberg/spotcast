"""Module to test the async_get_album function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    InternalSession,
    OAuth2Session,
    HomeAssistant,
    Spotify,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"

API_RESULT = {
    "album_type": "album",
    "total_tracks": 12,
    "external_urls": {
        "spotify": "https://open.spotify.com/album/5LflIRpgFkIkwXZHiXqyoX"
    },
    "href": ...,
    "id": "5LflIRpgFkIkwXZHiXqyoX",
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
    "name": "Bloodstone & Diamonds",
    "release_date": "2014-11-07",
    "release_date_precision": "day",
    "type": "album",
    "uri": "spotify:album:5LflIRpgFkIkwXZHiXqyoX",
    "artists": [
        {
            "external_urls": {
                "spotify": ...
            },
            "href": ...,
            "id": "0lVlNsuGaOr9vMHCZIAKMt",
            "name": "Machine Head",
            "type": "artist",
            "uri": "spotify:artist:0lVlNsuGaOr9vMHCZIAKMt"
        }
    ],
    "tracks": {
        "href": ...,
        "limit": 50,
        "next": None,
        "offset": 0,
        "previous": None,
        "total": 12,
        "items": [...]
    },
    "copyrights": [
        {
            "text": "2014 Nuclear Blast",
            "type": "C"
        },
        {
            "text": "2014 Nuclear Blast",
            "type": "P"
        }
    ],
    "external_ids": {
        "upc": "0727361332235"
    },
    "genres": [],
    "label": "Nuclear Blast",
    "popularity": 50,
    "is_playable": True
}


class TestPlayslistRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.return_value = API_RESULT

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            internal_session=self.mocks["internal"],
            external_session=self.mocks["external"],
        )

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.result = await self.account.async_get_album(
            "spotify:album:foo"
        )

    def test_proper_result_returned(self):
        self.assertEqual(API_RESULT, self.result)

    def test_proper_call_to__executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account._spotify.album,
                "foo",
                "CA",
            )
        except AssertionError:
            self.fail()
