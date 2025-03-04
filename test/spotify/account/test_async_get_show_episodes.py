"""Module to test the async_get_show_episodes function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PrivateSession,
    PublicSession,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestShowEpisodesRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            private_session=self.mocks["internal"],
            public_session=self.mocks["external"],
        )

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.account._async_pager = AsyncMock(
            return_value=["foo", "bar", "baz"]
        )

        self.result = await self.account.async_get_show_episodes(
            "spotify:show:foo"
        )

    def test_expected_result_received(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_pager_properly_called(self):
        try:
            self.account._async_pager.assert_called_with(
                function=self.account.apis["private"].show_episodes,
                prepends=["spotify:show:foo"],
                appends=["CA"],
                max_items=None,
            )
        except AssertionError:
            self.fail()
