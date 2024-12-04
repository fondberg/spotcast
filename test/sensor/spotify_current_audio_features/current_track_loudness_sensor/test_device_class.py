"""Module to test the device_class property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackLoudnessSensor,
    SensorDeviceClass,
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = CurrentTrackLoudnessSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(
            self.sensor.device_class,
            SensorDeviceClass.SOUND_PRESSURE
        )
