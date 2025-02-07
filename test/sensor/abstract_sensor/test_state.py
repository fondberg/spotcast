"""Module to test the state property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor
from custom_components.spotcast.spotify import SpotifyAccount


class DummySensor(SpotcastSensor):
    UNITS_OF_MEASURE = "foos"

    async def _async_update_process(self):
        ...


class TestSensorState(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)
        self.sensor._attr_state = 10

    def test_sensor_state_returned(self):
        self.assertEqual(self.sensor.state, 10)
