"""Module to test the build_from_integration function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.media_player.utils import (
    async_build_from_type,
    CastDevice,
    Chromecast,
    SpotifyDevice,
    UnknownIntegrationError,
    HomeAssistant,
    SpotifyAccount,
)


class DummyDevice:

    def __init__(self):
        pass


class TestCastDeviceCreation(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_cast_info = MagicMock()
        self.mock_cast_info.cast_type = "foo"

        self.mock_hass.async_add_executor_job = AsyncMock()

        self.mock_entity = MagicMock(spec=CastDevice)
        self.mock_entity._cast_info = MagicMock()
        self.mock_entity._cast_info.cast_info = self.mock_cast_info

        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)


class TestSpotifyDeviceCreation(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_entity = MagicMock(spec=SpotifyDevice)
        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIs(self.result, self.mock_entity)


class TestNoneManagedDeviceCreation(IsolatedAsyncioTestCase):

    async def test_error_raised(self):
        self.mock_entity = DummyDevice()
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_account = MagicMock(spec=SpotifyDevice)

        with self.assertRaises(UnknownIntegrationError):
            await async_build_from_type(
                self.mock_hass,
                self.mock_entity,
                self.mock_account,
            )
