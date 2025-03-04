"""Module to test the fetch_view function"""
from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestPlaylistRetrieval(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    def setUp(self, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )
        self.account._datasets["profile"] = MagicMock()
        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"].data = {
            "country": "CA"
        }

        self.account.apis["private"] = MagicMock()
        self.account.apis["private"]._get.return_value = ["foo", "bar", "baz"]

        self.result = self.account._fetch_view("content/foo", "fr")

    def test_proper_call_to_get(self):
        try:
            self.account.apis["private"]._get.assert_called_with(
                "content/foo",
                {
                    "content_limit": 25,
                    "locale": "fr",
                    "platform": "web",
                    "types": "album,playlist,artist,show,station",
                    "limit": 25,
                    "offset": 0,
                }
            )
        except AssertionError:
            self.fail()

    def test_expected_reply_returned(self):
        self.assertEqual(
            self.result,
            ["foo", "bar", "baz"],
        )
