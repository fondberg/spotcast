"""Module to test the async_play_from_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.play_from_search import (
    async_play_from_search,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

from test.services.play_from_search import TEST_MODULE


class TestPlayFromSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_play: AsyncMock,
    ):

        mock_entry.return_value = MagicMock(spec=ConfigEntry)
        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry.return_value,
            "account": mock_account.return_value,
        }

        self.mocks["call"].data = {
            "search_term": "foo",
            "item_types": ["track", "artist"],
        }

        self.mocks["account"].async_search = AsyncMock(return_value={
            "artists": [
                {"name": "foo", "uri": "spotify:artist:foo"}
            ],
            "tracks": [
                {"name": "foobar", "uri": "spotify:track:foobar"}
            ]
        })

        self.result = await async_play_from_search(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_proper_uri_in_call(self):
        self.assertEqual(
            self.mocks["call"].data.get("spotify_uri"),
            "spotify:artist:foo",
        )
