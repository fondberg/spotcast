"""Module to test the get_token function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    SpotifyOAuth,
    Spotify,
    NoAuthManagerError,
)


class TestOAuth2Session(TestCase):

    def setUp(self):
        self.oauth = MagicMock(spec=OAuth2Session)
        self.oauth.token = {
            "access_token": "12345"
        }
        self.account = SpotifyAccount.from_hass_oauth(self.oauth)

    def test_token_is_retrived(self):
        result = self.account.get_token()
        self.assertEqual(result, "12345")


class TestSpotifyAuth(TestCase):

    def setUp(self):
        self.oauth = MagicMock(spec=SpotifyOAuth)
        self.oauth.token = {
            "access_token": "12345"
        }
        self.account = SpotifyAccount.from_hass_oauth(self.oauth)

    def test_token_is_retrived(self):
        result = self.account.get_token()
        self.assertEqual(result, "12345")


class TestMissingAuthManager(TestCase):

    def setUp(self):
        self.spotify = MagicMock(spec=Spotify)
        self.spotify.token = {
            "access_token": "12345"
        }
        self.account = SpotifyAccount(self.spotify)

    def test_token_is_retrived(self):

        with self.assertRaises(NoAuthManagerError):
            self.account.get_token()
