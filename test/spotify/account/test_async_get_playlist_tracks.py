"""Module to test the get_playlist_tracks function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PrivateSession,
    PublicSession,
    Spotify,
)

from test.spotify.account import TEST_MODULE


class TestPlaylistTrackRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

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

        self.result = await self.account.async_get_playlist_tracks(
            "spotify:playlist:foo"
        )

    def test_expected_result_received(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_pager_properly_called(self):
        try:
            self.account._async_pager.assert_called_with(
                function=self.account.apis["private"].playlist_tracks,
                prepends=["foo", None],
                appends=["CA"]
            )
        except AssertionError:
            self.fail()
