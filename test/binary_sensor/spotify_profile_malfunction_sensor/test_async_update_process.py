"""Module to test the async_update_process method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.binary_sensor\
    .spotify_profile_malfunction_sensor import (
        SpotifyProfileMalfunctionBinarySensor,
    )


class TestNotImplemented(IsolatedAsyncioTestCase):

    async def test_error_raised(self):

        self.entity = SpotifyProfileMalfunctionBinarySensor(
            MagicMock(spec=SpotifyAccount)
        )

        with self.assertRaises(NotImplementedError):
            await self.entity._async_update_process()
