"""Module to test receive_message function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    CastMessage,
    UnknownMessageError,
)


class TestMessageManagement(TestCase):

    def setUp(self):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)

    @patch.object(SpotifyController, "_get_info_response_handler")
    def test_get_info_message(self, mock_handler: MagicMock):
        self.controller.receive_message(
            MagicMock(spec=CastMessage),
            {"type": self.controller.TYPE_GET_INFO_RESPONSE}
        )

        try:
            mock_handler.assert_called()
        except AssertionError:
            self.fail("Wrong handler called")

    @patch.object(SpotifyController, "_add_user_response_handler")
    def test_add_user_message(self, mock_handler: MagicMock):
        self.controller.receive_message(
            MagicMock(spec=CastMessage),
            {"type": self.controller.TYPE_ADD_USER_RESPONSE}
        )

        try:
            mock_handler.assert_called()
        except AssertionError:
            self.fail("Wrong handler called")

    @patch.object(SpotifyController, "_add_user_error_handler")
    def test_add_user_error(self, mock_handler: MagicMock):
        self.controller.receive_message(
            MagicMock(spec=CastMessage),
            {"type": self.controller.TYPE_ADD_USER_ERROR}
        )

        try:
            mock_handler.assert_called()
        except AssertionError:
            self.fail("Wrong handler called")

    @patch.object(SpotifyController, "_transfer_error_handler")
    def test_transfer_error(self, mock_handler: MagicMock):
        self.controller.receive_message(
            MagicMock(spec=CastMessage),
            {"type": self.controller.TYPE_TRANSFER_ERROR}
        )

        try:
            mock_handler.assert_called()
        except AssertionError:
            self.fail("Wrong handler called")

    def test_unknown_message(self):

        with self.assertRaises(UnknownMessageError):
            self.controller.receive_message(
                MagicMock(spec=CastMessage),
                {"type": "foo"}
            )
