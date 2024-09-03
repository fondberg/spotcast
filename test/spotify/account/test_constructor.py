"""Module to test the SpotifyAccount constructor"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from spotipy import Spotify

from custom_components.spotcast.spotify import SpotifyAccount


class TestDataRetention(TestCase):

    def setUp(self):

        self.spotify = MagicMock(spec=Spotify)

        self.account = SpotifyAccount(
            self.spotify,
            country="CA"
        )

    def test_country_value_is_retained(self):
        self.assertEqual(self.account.country, "CA")

    def test_name_set_to_default_none(self):
        self.assertIsNone(self.account.name)
