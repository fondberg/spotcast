"""Module to test the is_ready property"""

from unittest import TestCase
from time import time

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)


class TestIsReady(TestCase):

    def setUp(self):
        self.supervisor = RetrySupervisor()

    def test_is_ready(self):
        self.assertTrue(self.supervisor.is_ready)


class TestIsNotReady(TestCase):

    def setUp(self):
        self.supervisor = RetrySupervisor()
        self.supervisor._next_retry = time() + 9999

    def test_is_not_ready(self):
        self.assertFalse(self.supervisor.is_ready)
