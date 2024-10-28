"""Module to test the constructor of the spotify_controller class"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from threading import Event

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
)


class TestDataRetention(TestCase):

    def setUp(self):
        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(self.mock_account)

    def test_account_retained(self):
        self.assertEqual(self.controller.account, self.mock_account)

    def test_threanding_event_created(self):
        self.assertIsInstance(self.controller.waiting, Event)

    def test_is_launmched_set_to_false_by_default(self):
        self.assertFalse(self.controller.is_launched)

    def test_current_message_initialized_to_none(self):
        self.assertIsNone(self.controller._current_message)
