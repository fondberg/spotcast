"""Module to test the state_class property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.spotify_followers_sensor import (
    SpotifyFollowersSensor,
    SensorStateClass
)


class TestStateClassValue(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = SpotifyFollowersSensor(self.account)

    def test_state_class_is_set_to_measurements(self):
        self.assertEqual(self.sensor.state_class, SensorStateClass.MEASUREMENT)
