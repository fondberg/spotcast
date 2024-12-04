"""Module to test the constructor of the Spotify Account"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Dataset,
    Spotify,
)

from test.spotify.account import TEST_MODULE


class TestDataRetention(TestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    def setUp(self, mock_spotify: MagicMock):

        mock_internal = MagicMock(spec=PrivateSession)
        mock_external = MagicMock(spec=PublicSession)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=MagicMock(spec=HomeAssistant),
            public_session=mock_external,
            private_session=mock_internal,
            is_default=True
        )

    def test_sessions_contain_both_sessions(self):
        self.assertIn("public", self.account.sessions)
        self.assertIn("private", self.account.sessions)
        self.assertIsInstance(self.account.sessions["public"], PublicSession)
        self.assertIsInstance(
            self.account.sessions["private"],
            PrivateSession
        )

    def test_spotify_created_with_proper_auth(self):
        self.assertIn("public", self.account.apis)
        self.assertIn("private", self.account.apis)
        self.assertIsInstance(self.account.apis["public"], Spotify)
        self.assertIsInstance(
            self.account.apis["private"],
            Spotify,
        )

    def test_is_default_saved(self):
        self.assertTrue(self.account.is_default)

    def test_datasets_created(self):
        self.assertIsInstance(self.account._datasets, dict)

    def test_datasets_are_dataset_objects(self):
        for item in self.account._datasets.values():
            self.assertIsInstance(item, Dataset)

    def test_default_refresh_rate_set(self):
        self.assertEqual(self.account._base_refresh_rate, 30)

    def test_entry_id_saved(self):
        self.assertEqual(self.account.entry_id, "12345")
