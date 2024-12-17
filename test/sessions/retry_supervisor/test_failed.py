"""Module to test the failed function"""

from unittest import TestCase
from time import time

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)


class TestFailedRefresh(TestCase):

    def setUp(self):
        self.supervisor = RetrySupervisor()
        self.supervisor.failed()

    def test_next_retry_set_to_later(self):
        self.assertGreater(self.supervisor._next_retry, time())
