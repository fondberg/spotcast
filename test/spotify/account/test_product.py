"""Module to test the product property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestProductValue(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(sepc=OAuth2Session),
        }

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
        )

        self.account._profile = {
            "product": "premium"
        }

    def test_product_properly_returned(self):
        self.assertEqual(self.account.product, "premium")
