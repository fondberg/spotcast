"""Module to test the add_user_error_handler"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    CastMessage,
    AppLaunchError,
)

TEST_MODULE = "custom_components.spotcast.chromecast.spotify_controller"


class TestAddUserErrorHandling(TestCase):

    @patch(f"{TEST_MODULE}.threading.Event")
    def setUp(self, mock_event: MagicMock):

        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

        try:
            self.controller._add_user_error_handler(
                MagicMock(spec=CastMessage),
                {}
            )
        except AppLaunchError:
            pass

    def test_device_removed(self):
        self.assertIsNone(self.controller.device)

    def test_credential_error_set(self):
        try:
            self.controller.waiting.set.assert_called()
        except AssertionError:
            self.fail()

    def test_credentials_error_set(self):
        self.assertTrue(self.controller.credential_error)
