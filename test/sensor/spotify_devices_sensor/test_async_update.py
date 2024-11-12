"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_devices_sensor import (
    SpotifyDevicesSensor,
    ReadTimeoutError,
    STATE_UNKNOWN
)
from custom_components.spotcast.spotify import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyDevicesSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_devices.return_value = ["foo", "bar"]
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_devices.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, 2)

    def test_extra_attributes_properly_set(self):
        self.assertEqual(
            self.sensor.extra_state_attributes,
            {"devices": ["foo", "bar"]}
        )


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyDevicesSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_devices.side_effect = ReadTimeoutError(
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
            self.account.async_devices.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)

    def test_extra_attributes_resetted(self):
        self.assertEqual(self.sensor.extra_state_attributes, {"devices": []})
