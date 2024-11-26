"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_playlists_sensor import (
    SpotifyPlaylistsSensor,
    ReadTimeoutError,
    STATE_UNKNOWN
)
from custom_components.spotcast.spotify import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyPlaylistsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_playlists.return_value = [
            {
                "uri": "foo",
                "owner": {
                    "id": "dummy_id"
                },
                "images": [
                    {
                        "url": "https://localhost.com/2",
                        "height": 640,
                        "width": 640,
                    }
                ]
            }
        ]*10

        self.account.async_playlists_count.return_value = 11

        await self.sensor.async_update()

    def test_playlist_count_was_retrieved(self):
        try:
            self.account.async_playlists_count.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state__was_set_to_11(self):
        self.assertEqual(self.sensor.state, 11)


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyPlaylistsSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_playlists_count.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_playlists_count.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)
