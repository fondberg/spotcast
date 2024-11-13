"""Module to test the is_healthy property"""

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


class TestIsNotHealthy(TestCase):

    def setUp(self):
        self.session = DummySession()

    def test_is_not_healthy_by_default(self):
        self.assertFalse(self.session.is_healthy)


class TestIsHealthy(TestCase):

    def setUp(self):
        self.session = DummySession()
        self.session._is_healthy = True

    def test_is_healthy_when_set_true(self):
        self.assertTrue(self.session.is_healthy)
