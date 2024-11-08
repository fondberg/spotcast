"""Module to test the liked_songs_uri function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestLikedSongUriValue(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "internal": MagicMock(spec=OAuth2Session),
            "external": MagicMock(spec=InternalSession),
        }

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["internal"],
            internal_session=self.mocks["external"],
        )

        self.account._profile = {
            "id": "dummy_user"
        }

    def test_like_song_uri(self):
        self.assertEqual(
            self.account.liked_songs_uri,
            "spotify:user:dummy_user:collection",
        )
