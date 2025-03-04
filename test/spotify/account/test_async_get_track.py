"""Module to test the async_get_track function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PrivateSession,
    PublicSession,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestSongRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_ensure_tokens_valid")
    async def asyncSetUp(self, mock_valid: AsyncMock, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.track_info = {
            "album": {
                "album_type": "album",
                "total_tracks": 13,
                "external_urls": {
                    "spotify": "https://open.spotify.com/album/5l5m1hnH4punS1GQXgEi3T"
                },
                "href": "https://api.spotify.com/v1/albums/5l5m1hnH4punS1GQXgEi3T",
                "id": "5l5m1hnH4punS1GQXgEi3T",
                "images": [
                    {
                        "url": "https://i.scdn.co/image/ab67616d0000b273ca41a947c13b78749c4953b1",
                        "height": 640,
                        "width": 640
                    },
                    {
                        "url": "https://i.scdn.co/image/ab67616d00001e02ca41a947c13b78749c4953b1",
                        "height": 300,
                        "width": 300
                    },
                    {
                        "url": "https://i.scdn.co/image/ab67616d00004851ca41a947c13b78749c4953b1",
                        "height": 64,
                        "width": 64
                    }
                ],
                "name": "Lateralus",
                "release_date": "2001-05-15",
                "release_date_precision": "day",
                "type": "album",
                "uri": "spotify:album:5l5m1hnH4punS1GQXgEi3T",
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/2yEwvVSSSUkcLeSTNyHKh8"
                        },
                        "href": "https://api.spotify.com/v1/artists/2yEwvVSSSUkcLeSTNyHKh8",
                        "id": "2yEwvVSSSUkcLeSTNyHKh8",
                        "name": "TOOL",
                        "type": "artist",
                        "uri": "spotify:artist:2yEwvVSSSUkcLeSTNyHKh8"
                    }
                ],
                "is_playable": True
            },
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/2yEwvVSSSUkcLeSTNyHKh8"
                    },
                    "href": "https://api.spotify.com/v1/artists/2yEwvVSSSUkcLeSTNyHKh8",
                    "id": "2yEwvVSSSUkcLeSTNyHKh8",
                    "name": "TOOL",
                    "type": "artist",
                    "uri": "spotify:artist:2yEwvVSSSUkcLeSTNyHKh8"
                }
            ],
            "disc_number": 1,
            "duration_ms": 403533,
            "explicit": False,
            "external_ids": {
                "isrc": "USVR10100013"
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/track/55mJleti2WfWEFNFcBduhc"
            },
            "href": "https://api.spotify.com/v1/tracks/55mJleti2WfWEFNFcBduhc",
            "id": "55mJleti2WfWEFNFcBduhc",
            "is_playable": True,
            "name": "Schism",
            "popularity": 68,
            "preview_url": "https://p.scdn.co/mp3-preview/3c0d4ba93e1e771ef66c3a4326eac2dcb9e3244d?cid=cfe923b2d660439caf2b557b21f31221",
            "track_number": 5,
            "type": "track",
            "uri": "spotify:track:55mJleti2WfWEFNFcBduhc",
            "is_local": False
        }

        self.mocks["hass"].async_add_executor_job\
            .return_value = self.track_info

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

        self.result = await self.account.async_get_track(
            "spotify:track:55mJleti2WfWEFNFcBduhc"
        )

    def test_expected_track_info_returned(self):
        self.assertEqual(self.result, self.track_info)

    def test_executor_job_properly_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].track,
                "spotify:track:55mJleti2WfWEFNFcBduhc",
                "CA"
            )
        except AssertionError:
            self.fail()
