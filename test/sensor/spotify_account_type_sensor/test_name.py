"""Module to test the name property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.sensor.spotify_account_type_sensor"


class TestNameValue(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "device_info": MagicMock(spec=DeviceInfo),
        }

        self.mocks["account"].id = "dummy_account"
        self.mocks["account"].name = "Dummy Account"
        self.mocks["account"].device_info = self.mocks["device_info"]

        self.sensor = SpotifyAccountTypeSensor(self.mocks["account"])

    def test_name_value(self):
        self.assertEqual(
            self.sensor.name,
            "Dummy Account Spotify Account Type"
        )
