"""Module to test the async_wrapper"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    Spotify,
)


class TestMethodWrapping(IsolatedAsyncioTestCase):

    def setUp(self):
        spotify = MagicMock(spec=Spotify)
        self.account = SpotifyAccount(spotify)

    async def test_async_wtapper_runs_provided_method(self):

        mock_callable = MagicMock()

        await self.account._async_wrapper(mock_callable)

        try:
            mock_callable.assert_called_once()
        except AssertionError:
            self.fail(f"Function `{mock_callable}` was never called")

    async def test_arguments_are_ported_to_function(self):

        mock_callable = MagicMock()

        await self.account._async_wrapper(mock_callable, "foo", "bar")

        try:
            mock_callable.assert_called_with("foo", "bar")
        except AssertionError:
            self.fail("Function was not called with the expected arguments")
