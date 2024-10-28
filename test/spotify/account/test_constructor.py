"""Module to test the constructor of the Spotify Account"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)


class TestDataRetention(TestCase):

    @patch("custom_components.spotcast.spotify.account.Spotify")
    def setUp(self, mock_spotify: MagicMock):

        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            mock_external,
            mock_internal,
            "CA"
        )

    def test_sessions_contain_both_sessions(self):
        self.assertIn("external", self.account.sessions)
        self.assertIn("internal", self.account.sessions)
        self.assertIsInstance(self.account.sessions["external"], OAuth2Session)
        self.assertIsInstance(
            self.account.sessions["internal"],
            InternalSession
        )

    def test_spotify_created_with_proper_auth(self):
        try:
            self.mock_spotify.assert_called_with(
                auth="12345",
            )
        except AssertionError:
            self.fail("Spotify object didn't receive proper token'")

    def test_country_saved(self):
        self.assertEqual(self.account.country, "CA")

    def test_profile_is_declared(self):
        self.assertEqual(self.account._profile, {})
