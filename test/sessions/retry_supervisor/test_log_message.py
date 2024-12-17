"""Module to test the log_message function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import Logger, ERROR, DEBUG

from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor
)

TEST_MODULE = "custom_components.spotcast.sessions.retry_supervisor"


class TestFirstCommunication(TestCase):

    @patch(f"{TEST_MODULE}.LOGGER", spec=Logger)
    def setUp(self, mock_logger: MagicMock):

        self.logger = mock_logger
        self.supervisor = RetrySupervisor()
        self.supervisor.log_message("test")

    def test_log_error_message(self):
        try:
            self.logger.log.assert_called_with(ERROR, "test")
        except AssertionError:
            self.fail()

    def test_communication_counter_incremented(self):
        self.assertEqual(self.supervisor.communication_counter, 1)


class TestSubsequentCommunication(TestCase):

    @patch(f"{TEST_MODULE}.LOGGER", spec=Logger)
    def setUp(self, mock_logger: MagicMock):

        self.logger = mock_logger
        self.supervisor = RetrySupervisor()
        self.supervisor.communication_counter = 10
        self.supervisor.log_message("test")

    def test_log_error_message(self):
        try:
            self.logger.log.assert_called_with(DEBUG, "test")
        except AssertionError:
            self.fail()

    def test_communication_counter_incremented(self):
        self.assertEqual(self.supervisor.communication_counter, 11)
