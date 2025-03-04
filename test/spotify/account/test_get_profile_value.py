"""Module to test the get_profile_value function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestProfile(TestCase):

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

        self.profile = {
            "country": "CA",
            "display_name": "Dummy Account",
            "email": "dummy@email.com",
            "explicit_content": {
                "filter_enabled": False,
                "filter_locked": False
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/user/dummyaccount"
            },
            "followers": {
                "href": None,
                "total": 10
            },
            "href": "https://api.spotify.com/v1/users/dummyaccount",
            "id": "dummyaccount",
            "images": [
                {
                    "url": "https://dummy-image.com",
                    "height": 300,
                    "width": 300
                },
                {
                    "url": "https://dummy-image.com",
                    "height": 64,
                    "width": 64
                }
            ],
            "product": "premium",
            "type": "user",
            "uri": "spotify:user:dummyaccount"
        }
        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = self.profile

    def test_returns_expected_display_name(self):
        self.assertEqual(
            self.account.get_profile_value("display_name"),
            "Dummy Account"
        )
