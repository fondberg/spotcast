"""Module to test the profile property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestProfile(TestCase):

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
        self.result = self.account.profile

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, self.profile)
