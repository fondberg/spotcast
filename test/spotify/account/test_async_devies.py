"""Module to test the async_device method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    Spotify,
)


class TestAsyncDeviceCall(IsolatedAsyncioTestCase):

    def setUp(self):
        self.spotify = MagicMock(spec=Spotify)
        self.account = SpotifyAccount(self.spotify)

    async def test_device_method_is_called(self):
        self.spotify.devices.return_value = {
            "devices": [
                {
                    "name": "Mock_1",
                    "id": "12345"
                },
                {
                    "name": "Mock_2",
                    "id": "23456"
                }
            ]
        }

        result = await self.account.async_devices()

        self.assertEqual(len(result), 2)

        try:
            self.spotify.devices.assert_called_once()
        except AssertionError:
            self.fail("The function was never called")
