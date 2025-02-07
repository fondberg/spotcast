"""Module to test the constructor of the ConnectionSession"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
    HomeAssistant,
    ConfigEntry,
    Lock,
    RetrySupervisor,
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


class TestDataRetention(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
        }

        self.session = DummySession(
            hass=self.mocks["hass"],
            entry=self.mocks["entry"],
        )

    def test_hass_object_retained(self):
        self.assertIs(self.session.hass, self.mocks["hass"])

    def test_entry_object_retained(self):
        self.assertIs(self.session.entry, self.mocks["entry"])

    def test_lock_object_created(self):
        self.assertIsInstance(self.session._token_lock, Lock)

    def test_supervisor_created(self):
        self.assertIsInstance(self.session.supervisor, RetrySupervisor)

    def test_is_healthy_attribute_created(self):
        self.assertFalse(self.session._is_healthy)
