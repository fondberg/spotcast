"""Module to test the icon property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.const import STATE_UNKNOWN, STATE_ON, STATE_OFF

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.binary_sensor.abstract_binary_sensor import (
    SpotcastBinarySensor
)


class DummySensor(SpotcastBinarySensor):
    async def async_update(self):
        ...


class TestIconReturned(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)

    def test_unknown_state_icon(self):
        self.sensor._attr_state = STATE_UNKNOWN
        self.assertEqual(self.sensor.icon, "mdi:cube")

    def test_on_state_icon(self):
        self.sensor._attr_state = STATE_ON
        self.assertEqual(self.sensor.icon, "mdi:cube")

    def test_off_state_icon(self):
        self.sensor._attr_state = STATE_OFF
        self.assertEqual(self.sensor.icon, "mdi:cube-off")
