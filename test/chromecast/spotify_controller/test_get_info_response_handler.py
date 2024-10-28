"""Module to test the get_info_response_handler function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
    SpotifyAccount,
    CastMessage,
    HTTPError,
    AppLaunchError,
)


TEST_MODULE = "custom_components.spotcast.chromecast.spotify_controller"


class TestSuccessfulRequest(TestCase):

    @patch.object(SpotifyController, "send_message")
    @patch(f"{TEST_MODULE}.post")
    def setUp(self, mock_response: MagicMock, mock_send: MagicMock):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)
        self.mock_send = mock_send

        mock_account.get_token.return_value = "foo"

        mock_response.return_value.json.return_value = {
            "accessToken": "bar"
        }

        self.result = self.controller._get_info_response_handler(
            MagicMock(spec=CastMessage),
            {
                "payload": {
                    "clientID": "foo",
                    "deviceID": "baz"
                }
            }
        )

    def test_sent_proper_message(self):
        try:
            self.mock_send.assert_called_with({
                "type": self.controller.TYPE_ADD_USER,
                "payload": {
                    "blob": "bar",
                    "tokenType": "accessToken"
                }
            })
        except AssertionError:
            self.fail("Wrong data sent in message")

    def test_handler_returns_true(self):
        self.assertTrue(self.result)


class TestUnsuccessfulRequest(TestCase):

    @patch.object(SpotifyController, "send_message")
    @patch(f"{TEST_MODULE}.post")
    def test_raised_error_for_auth_failure(
            self,
            mock_response: MagicMock,
            mock_send: MagicMock
    ):
        mock_account = MagicMock(spec=SpotifyAccount)
        self.controller = SpotifyController(mock_account)
        self.mock_send = mock_send

        mock_account.get_token.return_value = "foo"

        mock_response.return_value.raise_for_status.side_effect = HTTPError()

        with self.assertRaises(AppLaunchError):
            self.controller._get_info_response_handler(
                MagicMock(spec=CastMessage),
                {
                    "payload": {
                        "clientID": "foo",
                        "deviceID": "baz"
                    }
                }
            )
