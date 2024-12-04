"""Module to test token property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ConfigEntry,
)


class TestAccessTokenValue(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)
        self.session = PrivateSession(mock_hass, mock_entry)
        self.session._access_token = "boo"

    def test_proper_value_returned(self):
        self.assertEqual(self.session.clean_token, "boo")
