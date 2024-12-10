"""Module to test the async_active_device function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock


from custom_components.spotcast.media_player.utils import (
    async_active_device,
    SpotifyAccount,
    SpotifyDevice,
    MissingActiveDeviceError,
)


class TestActiveDeviceExist(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_playback_state = AsyncMock(return_value={
            "device": {
                "id": "12345",
                "is_active": True,
                "is_private_session": False,
                "is_restricted": False,
                "name": "Dummy Device",
                "type": "computer",
                "volume_percent": 59,
                "supports_volume": True
            }
        })

        self.result = await async_active_device(self.mocks["account"])

    def test_device_returned_is_spotify_device(self):
        self.assertIsInstance(self.result, SpotifyDevice)

    def test_device_id_is_one_of_active_device(self):
        self.assertEqual(self.result.id, "12345")


class TestActiveDeviceDoesntExist(IsolatedAsyncioTestCase):

    async def test_error_raised(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_playback_state = AsyncMock(return_value={})

        with self.assertRaises(MissingActiveDeviceError):
            await async_active_device(self.mocks["account"])
