"""Module to test the id property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession
)


class TestPropertyValue(TestCase):

    def setUp(self):

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession)
        )

        self.account._profile["data"] = {
            "id": "dummy"
        }

    def test_id_value_returned(self):
        self.assertEqual(self.account.id, "dummy")
