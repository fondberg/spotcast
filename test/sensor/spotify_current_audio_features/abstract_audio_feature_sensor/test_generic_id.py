"""Module to test the _generic_id property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    AbstractAudioFeatureSensor
)


class TestGenericIdDefinition(TestCase):

    def setUp(self):
        self.sensor = AbstractAudioFeatureSensor(
            MagicMock(spec=SpotifyAccount)
        )

    def test_default_name(self):
        self.assertEqual(self.sensor._generic_id, "current_track_abstract")

    def test_redefined_name(self):
        self.sensor.FEATURE_NAME = "foo"
        self.assertEqual(self.sensor._generic_id, "current_track_foo")
