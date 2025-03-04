"""Module to test the get_token function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestDataRetention(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.run_coroutine_threadsafe")
    @patch(f"{TEST_MODULE}.Spotify")
    def setUp(
            self,
            mock_spotify: MagicMock,
            mock_coroutine: MagicMock,
            mock_store: MagicMock,
    ):

        mock_internal = MagicMock(spec=PrivateSession)
        mock_external = MagicMock(spec=PublicSession)
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_hass.loop = MagicMock()

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=mock_hass,
            public_session=mock_external,
            private_session=mock_internal,
            is_default=True
        )

        mock_coroutine.return_value.result.return_value = "12345"

        self.result = self.account.get_token("internal")

    def test_correct_token_retrieved(self):
        self.assertEqual(self.result, "12345")
