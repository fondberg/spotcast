"""Module to test the build_from_integration function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.media_player.utils import (
    build_from_type,
    CastDevice,
    Chromecast,
    SpotifyDevice,
    UnknownIntegrationError,
)


class DummyDevice:

    def __init__(self):
        pass


class TestCastDeviceCreation(TestCase):

    def setUp(self):

        self.mock_cast_info = MagicMock()
        self.mock_cast_info.cast_type = "foo"

        self.mock_entity = MagicMock(spec=CastDevice)
        self.mock_entity._cast_info = MagicMock()
        self.mock_entity._cast_info.cast_info = self.mock_cast_info

        self.result = build_from_type(self.mock_entity)

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)


class TestSpotifyDeviceCreation(TestCase):

    def setUp(self):

        self.mock_entity = MagicMock(spec=SpotifyDevice)
        self.result = build_from_type(self.mock_entity)

    def test_chromecast_device_returned(self):
        self.assertIs(self.result, self.mock_entity)


class TestNoneManagedDeviceCreation(TestCase):

    def test_error_raised(self):
        self.mock_entity = DummyDevice()

        with self.assertRaises(UnknownIntegrationError):
            build_from_type(self.mock_entity)
