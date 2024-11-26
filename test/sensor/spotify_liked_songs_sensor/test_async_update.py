"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_liked_songs_sensor import (
    SpotifyLikedSongsSensor,
    ReadTimeoutError,
    STATE_UNKNOWN
)
from custom_components.spotcast.spotify import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyLikedSongsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_liked_songs_count.return_value = 2

        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_liked_songs_count.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, 2)


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyLikedSongsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_liked_songs_count.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        self.sensor._attributes = {
            "devices": ["foo", "bar"]
        }

        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_liked_songs_count.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)
