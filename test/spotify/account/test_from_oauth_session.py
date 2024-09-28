"""Module to test the from_oauth_session method"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
)


class TestObjectCreation(TestCase):

    def setUp(self):

        session = MagicMock(spec=OAuth2Session)
        session.token = {
            "access_token": "123456"
        }
        self.account = SpotifyAccount.from_hass_oauth(session, "CA")

    def test_spotify_account_is_created(self):
        self.assertIsInstance(self.account, SpotifyAccount)
