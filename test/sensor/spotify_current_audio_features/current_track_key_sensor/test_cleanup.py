"""Module to test the _cleanup function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackKeySensor
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = CurrentTrackKeySensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_pitch_class_to_standard_notation(self):
        self.assertEqual(self.sensor._cleanup(2), "D")

    def test_no_key(self):
        self.assertEqual(self.sensor._cleanup(-1), "-")
