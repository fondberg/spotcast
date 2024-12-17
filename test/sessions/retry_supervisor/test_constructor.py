"""Module to test the constructor of ther RetrySupervisor"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)


class TestDataretention(TestCase):

    def setUp(self):
        self.supervisor = RetrySupervisor()

    def test_is_healthy_set_to_true(self):
        self.assertTrue(self.supervisor._is_healthy)

    def test_next_retry_set_to_zero(self):
        self.assertEqual(self.supervisor._next_retry, 0)

    def test_communication_counter_set_to_zero(self):
        self.assertEqual(self.supervisor.communication_counter, 0)
