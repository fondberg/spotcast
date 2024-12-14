"""Module to test the async_view function"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
)


class TestPlaylistRetrieval(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_ensure_tokens_valid")
    @patch.object(SpotifyAccount, "_async_pager")
    async def asyncSetUp(self, mock_pager: AsyncMock, mock_ensure: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "pager": mock_pager,
        }

        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )
        self.account._datasets["profile"] = MagicMock()
        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"].data = {
            "country": "CA"
        }

        self.result = await self.account.async_view("foo", "fr")

    def test_pager_properly_called(self):
        try:
            self.mocks["pager"].assert_called_with(
                function=self.account._fetch_view,
                prepends=["foo", "fr_CA"],
                limit=25,
                max_items=None,
                sub_layer="content",
            )
        except AssertionError:
            self.fail()

    def test_expected_result_returned(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])