"""Module to test the _cleanup function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackTimeSignatureSensor
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = CurrentTrackTimeSignatureSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_3_4_signature(self):
        self.assertEqual(self.sensor._cleanup(3), "3/4")
