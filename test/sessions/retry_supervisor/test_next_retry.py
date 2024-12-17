"""Module to test the next retry property"""

from unittest import TestCase

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)


class TestValueRetrieval(TestCase):

    def setUp(self):
        self.supervisor = RetrySupervisor()
        self.supervisor._next_retry = 9999

    def test_proper_value_returnmed(self):
        self.assertEqual(self.supervisor.next_retry, 9999)
