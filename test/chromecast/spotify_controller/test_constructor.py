"""Module to test constructor of the SpotifyController objectr"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from threading import Event

from spotipy import Spotify

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount
)


class TestDataRetention(TestCase):

    def setUp(self):
        self.account = SpotifyAccount(MagicMock(spec=Spotify))
        self.controller = SpotifyController(self.account)

    def test_account_was_retained(self):
        self.assertIs(self.controller.account, self.account)

    def test_event_thread_is_created(self):
        self.assertIsInstance(self.controller.waiting, Event)

    def test_is_launchedis_set_to_false(self):
        self.assertFalse(self.controller.is_launched)
