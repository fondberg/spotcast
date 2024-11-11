"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.sensor.spotify_profile_sensor import (
    SpotifyProfileSensor,
    ReadTimeoutError,
    STATE_UNKNOWN,
    STATE_OK,
)
from custom_components.spotcast import SpotifyAccount


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyProfileSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_profile.return_value = {
            "id": "dummy_id"
        }
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_OK)

    def test_extra_attributes_saved(self):
        self.assertEqual(
            self.sensor.extra_state_attributes,
            {"id": "dummy_id"},
        )


class TestUnsuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyProfileSensor(self.account)

        self.account.name = "Dummy Account"

        self.account.async_profile.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )

        self.sensor._attributes = {
            "id": "dummy_id"
        }
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)

    def test_extra_attributes_were_resetted(self):
        self.assertEqual(self.sensor.extra_state_attributes, {})
