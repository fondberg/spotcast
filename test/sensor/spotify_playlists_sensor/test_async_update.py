"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_playlists_sensor import (
    SpotifyPlaylistsSensor,
    ReadTimeoutError,
    STATE_UNKNOWN
)
from custom_components.spotcast import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyPlaylistsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_playlists.return_value = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
        ]
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_playlists.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, 11)

    def test_extra_attributes_saved(self):
        self.assertEqual(
            self.sensor.extra_state_attributes,
            {"first_10_playlists": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        )


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyPlaylistsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_playlists.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        self.sensor._attributes = {
            "first_10_playlists": [1, 2, 3]
        }

        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_playlists.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)

    def test_extra_attributes_were_resetted(self):
        self.assertEqual(
            self.sensor.extra_state_attributes,
            {"first_10_playlists": []}
        )
