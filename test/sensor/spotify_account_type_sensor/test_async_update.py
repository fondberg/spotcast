"""Module to test the async_update functio"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from urllib3.exceptions import ReadTimeoutError

from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
    SpotifyAccount,
    STATE_UNKNOWN,
)

TEST_MODULE = "custom_components.spotcast.sensor.spotify_account_type_sensor"


class TestIconValue(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.device_from_account")
    async def asyncSetUp(self, mock_device: MagicMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "device_info": MagicMock(spec=DeviceInfo),
            "profile_data": {
                "id": "dummy_account",
                "name": "Dummy Account",
                "type": "user",
            }

        }

        mock_device.return_value = self.mocks["device_info"]
        self.mocks["account"].id = "dummy_account"
        self.mocks["account"].async_profile = AsyncMock()
        self.mocks["account"].async_profile.return_value = self.mocks[
            "profile_data"
        ]

        self.sensor = SpotifyAccountTypeSensor(self.mocks["account"])

        await self.sensor.async_update()

    def test_profile_was_saved(self):
        self.assertEqual(self.sensor._profile, self.mocks["profile_data"])

    def test_profile_method_was_called(self):
        try:
            self.mocks["account"].async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_state_was_set_to_profile_type(self):
        self.assertEqual(self.sensor.state, "user")


class TestFailedUpdate(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.device_from_account")
    async def asyncSetUp(self, mock_device: MagicMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "device_info": MagicMock(spec=DeviceInfo),
            "profile_data": {
                "id": "dummy_account",
                "name": "Dummy Account",
                "type": "user",
            }

        }

        mock_device.return_value = self.mocks["device_info"]
        self.mocks["account"].id = "dummy_account"
        self.mocks["account"].async_profile = AsyncMock()
        self.mocks["account"].async_profile.side_effect = ReadTimeoutError(
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        self.sensor = SpotifyAccountTypeSensor(self.mocks["account"])

        await self.sensor.async_update()

    def test_attribute_set_to_unknown(self):
        self.assertEqual(self.sensor.state, STATE_UNKNOWN)
