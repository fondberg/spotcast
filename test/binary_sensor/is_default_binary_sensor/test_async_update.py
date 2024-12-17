"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.binary_sensor.is_default_binary_sensor import (
    IsDefaultBinarySensor
)


class TestDataUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.is_default = True
        self.account.entry_id = "1234"
        self.sensor = IsDefaultBinarySensor(self.account)
        await self.sensor.async_update()

    def test_state_set_to_on(self):
        self.assertTrue(self.sensor.is_on)
