"""Module to test the transfer_success_handler function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyAccount,
    SpotifyController,
    CastMessage,
)

TEST_MODULE = "custom_components.spotcast.chromecast.spotify_controller"


class TestTransferErrorHandling(TestCase):

    @patch(f"{TEST_MODULE}.threading.Event")
    def setUp(self, mock_event: MagicMock):

        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

        self.result = self.controller._transfer_success_handler(
            MagicMock(spec=CastMessage),
            {}
        )

    def test_handler_returns_true(self):
        self.assertTrue(self.result)
