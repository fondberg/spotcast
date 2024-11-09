"""Module to test the async_playlists"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestPlaylistRetrieval(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        mock_hass = MagicMock(spec=HomeAssistant)

        self.account = SpotifyAccount(
            mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.account._profile["data"] = {
            "id": "dummy",
            "name": "Dummy Profile"
        }

        mock_hass.async_add_executor_job = AsyncMock(
            side_effect=[
                {
                    "total": 4,
                    "items": [
                        "foo",
                        "bar",
                        "far"
                    ]
                },
                {
                    "total": 4,
                    "items": [
                        "boo"
                    ]
                }
            ]
        )

        self.result = await self.account.async_playlists()

    def test_received_expect_playlist_amount(self):
        self.assertEqual(len(self.result), 4)

    def test_playlist_received_are_expected(self):
        self.assertEqual(self.result, ["foo", "bar", "far", "boo"])
