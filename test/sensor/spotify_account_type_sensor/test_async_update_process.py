"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
)
from custom_components.spotcast.spotify import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyAccountTypeSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_profile.return_value = {
            "id": "dummy_id",
            "type": "user",
        }

        await self.sensor._async_update_process()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, "user")
