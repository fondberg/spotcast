"""Module to test the search account function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.utils import (
    search_account,
    HomeAssistant,
    AccountNotFoundError,
)


class TestAccountSearch(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account_a": MagicMock(spec=SpotifyAccount),
            "account_b": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account_a"]
                },
                "34567": {
                    "account": self.mocks["account_b"]
                }
            }
        }

        self.mocks["account_a"].id = "id_a"
        self.mocks["account_a"].name = "Name A"
        self.mocks["account_b"].id = "id_b"
        self.mocks["account_b"].name = "Name B"

    def test_entry_id_search(self):
        result = search_account(self.mocks["hass"], "12345")
        self.assertIs(result, self.mocks["account_a"])

    def test_spotify_id_search(self):
        result = search_account(self.mocks["hass"], "id_b")
        self.assertIs(result, self.mocks["account_b"])

    def test_spotify_name_search(self):
        result = search_account(self.mocks["hass"], "Name A")
        self.assertIs(result, self.mocks["account_a"])

    def test_missing_account(self):

        with self.assertRaises(AccountNotFoundError):
            search_account(self.mocks["hass"], "Name C")
