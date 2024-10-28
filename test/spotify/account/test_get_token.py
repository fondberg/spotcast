"""Module to test the threadsafe synchronous get_token function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant
)

TEST_MODULE = "custom_components.spotcast.spotify.account."


class TestThreadsafeFunctionCall(TestCase):

    @patch.object(SpotifyAccount, "async_get_token")
    @patch(TEST_MODULE+"run_coroutine_threadsafe")
    def setUp(self, mock_run: MagicMock, mock_token: MagicMock):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.mock_hass.loop = "bar"

        self.mock_run = mock_run
        self.mock_run.return_value.result.return_value = "foo"

        self.account = SpotifyAccount(
            hass=self.mock_hass,
            external_session=mock_external,
            internal_session=mock_internal,
            country="CA"
        )

        self.result = self.account.get_token("internal")

    def test_run_coroutine_called_with_proper_arguments(self):
        try:
            self.mock_run.assert_called()
        except AssertionError:
            self.fail("Function called with improper arguments")

    def test_curoutine_returns_exepcted_value(self):
        self.assertEqual(self.result, "foo")
