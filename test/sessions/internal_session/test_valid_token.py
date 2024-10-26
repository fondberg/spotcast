"""Module to test the valid_token property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession,
    CLOCK_OUT_OF_SYNC_MAX_SEC,
)


class TestInvalidToken(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")
        self.session._access_token = "boo"

    def test_invalid_if_expires_at_later_than_current_time(self):
        fake_expiration = 100
        self.session._expires_at = fake_expiration
        self.assertFalse(self.session.valid_token)


class TestValidToken(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")
        self.session._access_token = "boo"

    def test_invalid_if_expires_at_later_than_current_time(self):
        fake_expiration = time() + CLOCK_OUT_OF_SYNC_MAX_SEC + 200
        self.session._expires_at = fake_expiration
        self.assertTrue(self.session.valid_token)
