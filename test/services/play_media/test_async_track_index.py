"""Module to test the async_track_index function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_media import (
    async_track_index,
    SpotifyAccount,
)


class TestSingleDiscAlbum(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_get_track = AsyncMock()
        self.mocks["account"].async_get_track.return_value = {
            "disc_number": 1,
            "track_number": 5,
            "album": {
                "uri": "spotify:album:foo"
            }
        }

        self.uri, self.index = await async_track_index(
            self.mocks["account"],
            "spotify:track:bar",
        )

    def test_proper_order_of_tuple_object(self):
        self.assertIsInstance(self.uri, str)
        self.assertIsInstance(self.index, int)

    def test_correct_uri_returned(self):
        self.assertEqual(self.uri, "spotify:album:foo")

    def test_currect_index_returned(self):
        self.assertEqual(self.index, 4)


class TestMultiDiscAlbum(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_get_track = AsyncMock()
        self.mocks["account"].async_get_track.return_value = {
            "disc_number": 2,
            "track_number": 5,
            "album": {
                "uri": "spotify:album:foo"
            }
        }

        self.mocks["account"].async_get_album = AsyncMock()
        self.mocks["account"].async_get_album.return_value = {
            "tracks": {
                "items": [
                    {"uri": "spotify:track:chasing-shadows"},
                    {"uri": "spotify:track:midnight-serenade"},
                    {"uri": "spotify:track:crimson-harmony"},
                    {"uri": "spotify:track:echoes-of-dawn"},
                    {"uri": "spotify:track:whispered-lullaby"},
                    {"uri": "spotify:track:stellar-dreams"},
                    {"uri": "spotify:track:rising-tide"},
                    {"uri": "spotify:track:bar"},
                    {"uri": "spotify:track:forgotten-anthem"},
                    {"uri": "spotify:track:wandering-spirit"},
                    {"uri": "spotify:track:golden-reverie"},
                    {"uri": "spotify:track:fractured-melody"},
                    {"uri": "spotify:track:lost-horizons"},
                    {"uri": "spotify:track:serenade-of-starlight"},
                    {"uri": "spotify:track:eternal-drift"},
                ]
            }
        }

        self.uri, self.index = await async_track_index(
            self.mocks["account"],
            "spotify:track:bar",
        )

    def test_proper_order_of_tuple_object(self):
        self.assertIsInstance(self.uri, str)
        self.assertIsInstance(self.index, int)

    def test_correct_uri_returned(self):
        self.assertEqual(self.uri, "spotify:album:foo")

    def test_currect_index_returned(self):
        self.assertEqual(self.index, 7)
