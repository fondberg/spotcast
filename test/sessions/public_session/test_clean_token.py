"""Module to test the token property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.public_session import (
    PublicSession,
    OAuth2Session,
    ConfigEntry
)


class TestTokenValue(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_implementation = MagicMock(spec=OAuth2Session)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": {
                    "access_token": "boo"
                }
            }
        }

        self.session = PublicSession(
            hass=mock_hass,
            entry=mock_entry,
            implementation=mock_implementation
        )

    def test_token_value(self):
        self.assertEqual(self.session.clean_token, "boo")
