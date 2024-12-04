"""Module to test the _cleanup function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    AbstractAudioFeatureSensor
)


class TestCleanup(TestCase):

    def setUp(self):
        self.sensor = AbstractAudioFeatureSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_all_values_unchanged(self):

        values = [42, 3.1415, "foo", False]

        for value in values:
            self.assertEqual(self.sensor._cleanup(value), value)
