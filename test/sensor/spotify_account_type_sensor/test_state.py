"""Module to test the state propeorty"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.sensor.spotify_account_type_sensor"


class TestNameValue(TestCase):

    @patch(f"{TEST_MODULE}.device_from_account")
    def setUp(self, mock_device: MagicMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "device_info": MagicMock(spec=DeviceInfo),
        }

        mock_device.return_value = self.mocks["device_info"]
        self.mocks["account"].id = "dummy_account"
        self.mocks["account"].name = "Dummy Account"

        self.sensor = SpotifyAccountTypeSensor(self.mocks["account"])
        self.sensor._attr_state = "dummy_state"

    def test_state_property_mirrors_attribute(self):
        self.assertEqual(self.sensor.state, self.sensor._attr_state)
