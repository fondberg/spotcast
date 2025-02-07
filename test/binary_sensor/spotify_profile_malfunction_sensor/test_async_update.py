"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from urllib3.exceptions import ReadTimeoutError

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.binary_sensor\
    .spotify_profile_malfunction_sensor import (
        SpotifyProfileMalfunctionBinarySensor,
    )


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.is_default = True
        self.sensor = SpotifyProfileMalfunctionBinarySensor(self.account)
        await self.sensor.async_update()

    def test_state_set_to_on(self):
        self.assertFalse(self.sensor.is_on)


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.is_default = True
        self.sensor = SpotifyProfileMalfunctionBinarySensor(self.account)
        self.account.async_profile.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        await self.sensor.async_update()

    def test_state_set_to_on(self):
        self.assertTrue(self.sensor.is_on)
