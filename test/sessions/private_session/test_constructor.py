"""Module to test the PrivateSession constructor"""

from unittest import TestCase
from unittest.mock import MagicMock
from asyncio import Lock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    ConfigEntry
)


class TestDataRetention(TestCase):

    def setUp(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.session = PrivateSession(self.mock_hass, self.mock_entry)

    def test_hass_retained(self):
        self.assertIs(self.session.hass, self.mock_hass)

    def test_entry_retained(self):
        self.assertIs(self.session.entry, self.mock_entry)

    def test_access_token_set_to_none(self):
        self.assertIsNone(self.session._access_token)

    def test_expiration_set_to_zero(self):
        self.assertEqual(self.session._expires_at, 0)

    def test_lock_created_for_session(self):
        self.assertIsInstance(self.session._token_lock, Lock)
