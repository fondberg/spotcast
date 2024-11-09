"""Module to test the constructor of the SpotifyAccountTypeSensor"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
    SpotifyAccount,
    STATE_UNKNOWN,
)

TEST_MODULE = "custom_components.spotcast.sensor.spotify_account_type_sensor"


class TestDataRetention(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "device_info": MagicMock(spec=DeviceInfo),
        }

        self.mocks["account"].id = "dummy_account"
        self.mocks["account"].device_info = self.mocks["device_info"]

        self.sensor = SpotifyAccountTypeSensor(self.mocks["account"])

    def test_account_is_saved(self):
        self.assertIs(self.sensor.account, self.mocks["account"])

    def test_device_info_created(self):
        self.assertIs(self.sensor._attr_device_info, self.mocks["device_info"])

    def test_state_set_to_unknown(self):
        self.assertEqual(self.sensor._attr_state, STATE_UNKNOWN)

    def test_entity_id_created(self):
        self.assertEqual(
            self.sensor.entity_id,
            "sensor.dummy_account_spotify_account_type",
        )

    def test_profile_attribute_created(self):
        self.assertEqual(self.sensor._profile, {})
