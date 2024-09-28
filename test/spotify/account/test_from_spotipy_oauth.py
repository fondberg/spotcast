"""Module to test the from_spotipy_oauth static method"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    SpotifyOAuth
)


class TestAccountCreation(TestCase):

    def setUp(self):
        mock_oauth = MagicMock(spec=SpotifyOAuth)
        self.account = SpotifyAccount.from_spotipy_oauth(mock_oauth, "CA")

    def test_account_is_created(self):
        self.assertIsInstance(self.account, SpotifyAccount)

    def test_country_is_ported(self):
        self.assertEqual(self.account.country, "CA")
