"""Module to test the nase_refresh_rate proerty"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestGetter(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    def setUp(self, mock_spotify: MagicMock, mock_store: MagicMock):

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

    def test_refresh_rate_retrieved(self):
        self.assertEqual(
            self.account._base_refresh_rate,
            self.account.base_refresh_rate,
        )


class TestSetter(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    def setUp(self, mock_spotify: MagicMock, mock_store: MagicMock):

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

        self.account.base_refresh_rate = 45

    def test_refresh_rate_updated(self):
        self.assertEqual(self.account.base_refresh_rate, 45)

    def test_datasets_were_updated(self):
        self.account._datasets["profile"].refresh_rate = 450
