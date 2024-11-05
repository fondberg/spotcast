"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice,
    SpotifyAccount,
)


class TestUnavailable(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            }
        )

        self.device._is_unavailable = True

        self.result = await self.device.async_update()

    async def test_skipping_update(self):
        try:
            self.mock_account.async_devices.assert_not_called()
        except AssertionError:
            self.fail()


class TestAvailable(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_devices = AsyncMock()
        self.mock_devices.return_value = [
            {
                "id": "89675",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            },
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": False,
            }
        ]

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"
        self.mock_account.async_devices = self.mock_devices

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            }
        )

        self.result = await self.device.async_update()

    async def test_update_called(self):
        try:
            self.mock_devices.assert_called()
        except AssertionError:
            self.fail()

    async def test_device_is_inactive(self):
        self.assertFalse(self.device._device_data["is_active"])


class TestDeviceMissing(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_devices = AsyncMock()
        self.mock_devices.return_value = [
            {
                "id": "89675",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            },
        ]

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"
        self.mock_account.async_devices = self.mock_devices

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            }
        )

        self.result = await self.device.async_update()

    async def test_update_called(self):
        try:
            self.mock_devices.assert_called()
        except AssertionError:
            self.fail()

    async def test_device_is_inactive(self):
        self.assertTrue(self.device._device_data["is_active"])
