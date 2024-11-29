"""Module to test the cookies property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ConfigEntry
)


class TestCookieValue(TestCase):

    def setUp(self):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(mock_hass, mock_entry)
        self.cookies = self.session.cookies

    def test_sp_dc_key_in_cookie_dict(self):
        self.assertIn("sp_dc", self.cookies)

    def test_sp_key_key_in_cookie_dict(self):
        self.assertIn("sp_key", self.cookies)

    def test_sp_dc_set_to_proper_value(self):
        self.assertEqual(self.cookies["sp_dc"], "foo")

    def test_sp_key_set_to_proper_value(self):
        self.assertEqual(self.cookies["sp_key"], "bar")
