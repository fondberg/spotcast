"""Module to test the nase_refresh_rate proerty"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    Dataset
)


class TestGetter(TestCase):

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
            entry_id="12345",
            hass=MagicMock(spec=HomeAssistant),
            external_session=mock_external,
            internal_session=mock_internal,
            is_default=True
        )

    def test_refresh_rate_retrieved(self):
        self.assertEqual(
            self.account._base_refresh_rate,
            self.account.base_refresh_rate,
        )


class TestSetter(TestCase):

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
            entry_id="12345",
            hass=MagicMock(spec=HomeAssistant),
            external_session=mock_external,
            internal_session=mock_internal,
            is_default=True
        )

        self.account.base_refresh_rate = 45

    def test_refresh_rate_updated(self):
        self.assertEqual(self.account.base_refresh_rate, 45)

    def test_datasets_were_updated(self):
        self.account._datasets["profile"].refresh_rate = 450
