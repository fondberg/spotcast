"""Module to test the state property of thge SpotifyDevice class"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice,
    SpotifyAccount,
    STATE_ON,
    STATE_OFF,
    STATE_UNAVAILABLE,
)


class TestOn(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": True,
            }
        )

    def test_state_is_on(self):
        self.assertEqual(self.device.state, STATE_ON)


class TestOff(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": False,
            }
        )

    def test_state_is_on(self):
        self.assertEqual(self.device.state, STATE_OFF)


class TestUnavailable(TestCase):

    def setUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_account.id = "dummy"
        self.mock_account.name = "Dummy User"

        self.device = SpotifyDevice(
            self.mock_account,
            {
                "id": "12345",
                "name": "dummy_device",
                "type": "dummy",
                "is_active": False,
            }
        )

        self.device._is_unavailable = True

    def test_state_is_on(self):
        self.assertEqual(self.device.state, STATE_UNAVAILABLE)
