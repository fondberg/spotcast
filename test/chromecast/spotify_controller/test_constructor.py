"""Module to test constructor of the SpotifyController objectr"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from spotipy import Spotify

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount
)


class TestDataRetention(TestCase):

    def test_pass(self):
        ...
