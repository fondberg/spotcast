"""Module to test the InternalSession constructor"""

from unittest import TestCase
from unittest.mock import MagicMock
from asyncio import Lock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession
)


class TestDataRetention(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")

    def test_hass_retained(self):
        self.assertIsInstance(self.session.hass, HomeAssistant)

    def test_sp_dc_retained(self):
        self.assertEqual(self.session.sp_dc, "foo")

    def test_sp_key_retained(self):
        self.assertEqual(self.session.sp_key, "bar")

    def test_access_token_set_to_none(self):
        self.assertIsNone(self.session._access_token)

    def test_expiration_set_to_zero(self):
        self.assertEqual(self.session._expires_at, 0)

    def test_lock_created_for_session(self):
        self.assertIsInstance(self.session._token_lock, Lock)
