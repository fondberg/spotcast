"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.media_player.device_manager import (
    DeviceManager,
    SpotifyAccount,
    SpotifyDevice,
    AddEntitiesCallback,
)


class TestNewDevices(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_callack = MagicMock(spec=AddEntitiesCallback)

        self.mock_account.async_devices = AsyncMock(
            return_value=[
                {
                    "id": "1234",
                    "name": "dummy device",
                    "type": "Computer",
                }
            ]
        )

        self.device_manager = DeviceManager(
            self.mock_account,
            self.mock_callack,
        )

        await self.device_manager.async_update()

    async def test_device_added_to_tracked(self):
        self.assertEqual(len(self.device_manager.tracked_devices), 1)
        self.assertIn("1234", self.device_manager.tracked_devices)

    async def test_entity_was_added(self):
        try:
            self.mock_callack.assert_called()
        except AssertionError:
            self.fail()


class TestIgnoredDevice(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_callack = MagicMock(spec=AddEntitiesCallback)

        self.mock_account.async_devices = AsyncMock(
            return_value=[
                {
                    "id": "1234",
                    "name": "dummy device",
                    "type": "CastAudio",
                }
            ]
        )

        self.device_manager = DeviceManager(
            self.mock_account,
            self.mock_callack,
        )

        await self.device_manager.async_update()

    async def test_no_devices_added(self):
        self.assertEqual(len(self.device_manager.tracked_devices), 0)


class TestAlreadyTrackedDevice(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_callack = MagicMock(spec=AddEntitiesCallback)

        self.mock_account.async_devices = AsyncMock(
            return_value=[
                {
                    "id": "1234",
                    "name": "dummy device",
                    "type": "Computer",
                }
            ]
        )

        self.device_manager = DeviceManager(
            self.mock_account,
            self.mock_callack,
        )

        self.device_manager.tracked_devices = {
            "1234": MagicMock(spec=SpotifyDevice)
        }

        await self.device_manager.async_update()

    async def test_no_devices_added(self):
        self.assertEqual(len(self.device_manager.tracked_devices), 1)

    async def test_add_entity_not_called(self):
        try:
            self.mock_callack.assert_not_called()
        except AssertionError:
            self.fail()


class TestRemovedDevice(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_callack = MagicMock(spec=AddEntitiesCallback)

        self.mock_account.async_devices = AsyncMock(return_value=[])

        self.device_manager = DeviceManager(
            self.mock_account,
            self.mock_callack,
        )

        self.device_manager.tracked_devices = {
            "1234": MagicMock(spec=SpotifyDevice)
        }

        await self.device_manager.async_update()

    async def test_device_removed_from_tracked(self):
        self.assertEqual(len(self.device_manager.tracked_devices), 0)
