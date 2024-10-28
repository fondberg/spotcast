"""Module to test the add_user_response_handler"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    CastMessage,
)

TEST_MODULE = "custom_components.spotcast.chromecast.spotify_controller"


class TestAddUserresponseHandling(TestCase):

    @patch(f"{TEST_MODULE}.threading.Event")
    def setUp(self, mock_event: MagicMock):

        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

        self.result = self.controller._add_user_response_handler(
            MagicMock(spec=CastMessage),
            {}
        )

    def test_is_launched_set_true(self):
        self.assertTrue(self.controller.is_launched)

    def test_event_thread_set(self):
        try:
            self.controller.waiting.set.assert_called()
        except AssertionError:
            self.fail()

    def test_handler_returns_true(self):
        self.assertTrue(self.result)
