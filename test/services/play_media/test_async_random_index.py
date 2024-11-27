"""Module to test the get_ranom_index function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_media import (
    async_random_index,
    SpotifyAccount,
    ServiceValidationError,
)

TEST_MODULE = "custom_components.spotcast.services.play_media"


class TestAlbumRandInt(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.randint", new_callable=MagicMock)
    async def asyncSetUp(self, mock_random: MagicMock):

        mock_random.return_value = 5

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_get_album = AsyncMock()
        self.mocks["account"].async_get_album.return_value = {
            "total_tracks": 10
        }

        self.resut = await async_random_index(
            self.mocks["account"],
            "spotify:album:foo",
        )

    def test_received_expected_index(self):
        self.assertEqual(self.resut, 5)

    def test_get_album_called(self):
        try:
            self.mocks["account"].async_get_album.assert_called()
        except AssertionError:
            self.fail()


class TestPlaylistRandInt(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.randint", new_callable=MagicMock)
    async def asyncSetUp(self, mock_random: MagicMock):

        mock_random.return_value = 42

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_get_playlist = AsyncMock()
        self.mocks["account"].async_get_playlist.return_value = {
            "tracks": {
                "total": 50
            }
        }
        self.resut = await async_random_index(
            self.mocks["account"],
            "spotify:playlist:foo",
        )

    def test_received_expected_index(self):
        self.assertEqual(self.resut, 42)

    def test_get_artist_called(self):
        try:
            self.mocks["account"].async_get_playlist.assert_called()
        except AssertionError:
            self.fail()


class TestUserLikedSongs(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.randint", new_callable=MagicMock)
    async def asyncSetUp(self, mock_random: MagicMock):

        mock_random.return_value = 314

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_liked_songs_count = AsyncMock()
        self.mocks["account"].liked_songs_uri = "spotify:user:foo:collection"
        self.mocks["account"].async_liked_songs_count.return_value = 500
        self.resut = await async_random_index(
            self.mocks["account"],
            "spotify:user:foo:collection",
        )

    def test_received_expected_index(self):
        self.assertEqual(self.resut, 314)

    def test_get_artist_called(self):
        try:
            self.mocks["account"].async_liked_songs_count.assert_called()
        except AssertionError:
            self.fail()


class TestInvalidContextUri(IsolatedAsyncioTestCase):

    async def test_error_raised(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        with self.assertRaises(ServiceValidationError):
            self.resut = await async_random_index(
                self.mocks["account"],
                "spotify:track:foo",
            )
