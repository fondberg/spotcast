"""Module to test the stop_app function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    Chromecast,
)


class TestStoppingApp(TestCase):

    def setUp(self):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_device = MagicMock(spec=Chromecast)
        self.controller = SpotifyController(mock_account)

        self.controller.stop_app(self.mock_device)

    def test_quit_app_was_called(self):
        try:
            self.mock_device.quit_app.assert_called()
        except AssertionError:
            self.fail("quite_app was never called")

    def test_is_launched_set_to_false(self):
        self.assertFalse(self.controller.is_launched)
