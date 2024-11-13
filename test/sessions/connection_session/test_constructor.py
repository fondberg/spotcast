"""Module to test the constructor of the ConnectionSession"""

from unittest import TestCase

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession
)


class DummySession(ConnectionSession):

    async def async_ensure_token_valid(self):
        raise NotImplementedError

    @property
    def token(self):
        raise NotImplementedError


class TestDataRetention(TestCase):

    def setUp(self):

        self.session = DummySession()

    def test_is_healthy_attribute_created(self):
        self.assertFalse(self.session._is_healthy)
