"""Module to test the cookies property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession
)


class TestCookieValue(TestCase):

    def setUp(self):

        mock_hass = MagicMock(spec=HomeAssistant)

        self.session = InternalSession(mock_hass, "foo", "bar")
        self.cookies = self.session.cookies

    def test_sp_dc_key_in_cookie_dict(self):
        self.assertIn("sp_dc", self.cookies)

    def test_sp_key_key_in_cookie_dict(self):
        self.assertIn("sp_key", self.cookies)

    def test_sp_dc_set_to_proper_value(self):
        self.assertEqual(self.cookies["sp_dc"], "foo")

    def test_sp_key_set_to_proper_value(self):
        self.assertEqual(self.cookies["sp_key"], "bar")
