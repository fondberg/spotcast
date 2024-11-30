"""Module to test the _cleanup function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackModeSensor
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = CurrentTrackModeSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_major_key(self):
        self.assertEqual(self.sensor._cleanup(1), "major")

    def test_minor_key(self):
        self.assertEqual(self.sensor._cleanup(0), "minor")
