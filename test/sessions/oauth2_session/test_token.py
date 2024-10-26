"""Module to test the token property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.oauth2_session import (
    OAuth2Session,
    AbstractOAuth2Implementation,
    ConfigEntry
)


class TestTokenValue(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_implementation = MagicMock(spec=AbstractOAuth2Implementation)
        mock_entry = MagicMock(spec=ConfigEntry)
        mock_entry.data = {
            "external_api": {
                "token": "boo"
            }
        }

        self.session = OAuth2Session(
            hass=mock_hass,
            config_entry=mock_entry,
            implementation=mock_implementation
        )

    def test_token_value(self):
        self.assertEqual(self.session.token, "boo")
