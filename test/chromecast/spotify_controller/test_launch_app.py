"""Module to test the launch_app function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from threading import Event

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    Chromecast,
    AppLaunchError,
)

TEST_MODULE = "custom_components.spotcast.chromecast.spotify_controller."


class TestAppLaunch(TestCase):

    @patch.object(SpotifyController, "launch")
    def test_app_launch_returns(self, mock_launch: MagicMock):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

        mock_launch.side_effect = self.set_is_launched

        mock_device = MagicMock(spec=Chromecast)

        try:
            self.controller.launch_app(mock_device, max_attempts=2)
        except AppLaunchError:
            self.fail("Failed to launch app")

    def set_is_launched(self, *_, **__):
        self.controller.is_launched = True


class TestAppFailLaunch(TestCase):

    @patch(TEST_MODULE+"threading.Event", spec=Event)
    @patch.object(SpotifyController, "launch")
    def test_app_launch_fails(
            self,
            mock_launch: MagicMock,
            mock_event: MagicMock
    ):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

        mock_event.wait.side_effect = [
            None,
            self.set_is_launched,
        ]

        mock_device = MagicMock(spec=Chromecast)

        with self.assertRaises(AppLaunchError):
            self.controller.launch_app(mock_device, max_attempts=2)

    def set_is_launched(self, *_, **__):
        self.controller.is_launched = True
