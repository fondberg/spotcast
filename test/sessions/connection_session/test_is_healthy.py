"""Module to test the is_healthy property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
    HomeAssistant,
    ConfigEntry,
)


class DummySession(ConnectionSession):

    async def async_ensure_token_valid(self):
        raise NotImplementedError

    @property
    def token(self):
        raise NotImplementedError

    @property
    def clean_token(self):
        raise NotImplementedError


class TestIstHealthy(TestCase):

    def setUp(self):
        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
        }
        self.session = DummySession(
            hass=self.mocks["hass"],
            entry=self.mocks["entry"]
        )

    def test_is_not_healthy_by_default(self):
        self.assertTrue(self.session.is_healthy)


class TestIsNotHealthy(TestCase):

    def setUp(self):
        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
        }
        self.session = DummySession(
            hass=self.mocks["hass"],
            entry=self.mocks["entry"]
        )
        self.session.supervisor._is_healthy = False

    def test_is_healthy_when_set_true(self):
        self.assertFalse(self.session.is_healthy)
