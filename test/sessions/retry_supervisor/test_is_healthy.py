"""Module to test the is_healthy property"""

from unittest import TestCase
from time import time

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)


class TestNotHealthy(TestCase):

    def setUp(self):

        self.supervisor = RetrySupervisor()
        self.supervisor.is_healthy = False

    def test_is_not_healthy(self):
        self.assertFalse(self.supervisor.is_healthy)

    def test_next_retry_set_to_later(self):
        self.assertGreater(self.supervisor._next_retry, time())


class TestHealthy(TestCase):

    def setUp(self):

        self.supervisor = RetrySupervisor()
        self.supervisor.communication_counter = 10
        self.supervisor._next_retry = 9999
        self.supervisor.is_healthy = True

    def test_is_healthy(self):
        self.assertTrue(self.supervisor.is_healthy)

    def test_communication_counter_reset(self):
        self.assertEqual(self.supervisor.communication_counter, 0)

    def test_next_retry_reset(self):
        self.assertEqual(self.supervisor._next_retry, 0)
