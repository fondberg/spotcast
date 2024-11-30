"""Module to test the name property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    AbstractAudioFeatureSensor
)


class TestNameDefinition(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.name = "Foo"
        self.sensor = AbstractAudioFeatureSensor(self.account)

    def test_default_name(self):
        self.assertEqual(
            self.sensor.name,
            "Spotcast - Foo Current Track Abstract"
        )

    def test_redefined_name(self):
        self.sensor.FEATURE_NAME = "hello_world"
        self.assertEqual(
            self.sensor.name,
            "Spotcast - Foo Current Track Hello World",
        )
