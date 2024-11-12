"""Module to test the icon property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.const import STATE_UNKNOWN, STATE_ON, STATE_OFF

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor
from custom_components.spotcast.spotify import SpotifyAccount


class DummySensor(SpotcastSensor):
    UNITS_OF_MEASURE = "foos"

    async def async_update(self):
        ...


class TestIconValue(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)

    def test_unknown_state(self):
        self.sensor._attr_state = STATE_UNKNOWN
        self.assertEqual(self.sensor.icon, "mdi:cube")

    def test_inactive_state(self):
        self.sensor._attr_state = STATE_OFF
        self.assertEqual(self.sensor.icon, "mdi:cube-off")

    def test_active_state(self):
        self.sensor._attr_state = STATE_ON
        self.assertEqual(self.sensor.icon, "mdi:cube")

    def test_zero_state(self):
        self.sensor._attr_state = 0
        self.assertEqual(self.sensor.icon, "mdi:cube-off")

    def test_numeric_state(self):
        self.sensor._attr_state = 10
        self.assertEqual(self.sensor.icon, "mdi:cube")
