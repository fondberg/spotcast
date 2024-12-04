"""Module to test the _cleanup function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    AbstractPercentSensor
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = AbstractPercentSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_percentage_changed_to_human_readable(self):
        self.assertEqual(self.sensor._cleanup(0.31415), 31.415)
