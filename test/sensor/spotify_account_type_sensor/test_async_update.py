"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
    ReadTimeoutError,
    STATE_UNKNOWN
)
from custom_components.spotcast import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyAccountTypeSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_profile.return_value = {
            "id": "dummy_id",
            "type": "user",
        }

        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, "user")


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyAccountTypeSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_profile.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)
