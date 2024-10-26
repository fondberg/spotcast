"""Module to test token property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.internal_session import (
    InternalSession
)


class TestAccessTokenValue(TestCase):

    def setUp(self):
        mock_hass = MagicMock(spec=HomeAssistant)
        self.session = InternalSession(mock_hass, "foo", "bar")
        self.session._access_token = "boo"

    def test_proper_value_returned(self):
        self.assertEqual(self.session.token, "boo")
