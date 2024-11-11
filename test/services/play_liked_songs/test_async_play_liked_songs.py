"""Module to test the async_play_liked_songs function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_liked_songs import (
    async_play_liked_songs,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_liked_songs"


class TestLikedSongsPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
        self,
        mock_play: AsyncMock,
        mock_account: AsyncMock,
        mock_entry: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": HomeAssistant,
            "call": ServiceCall,
            "account": mock_account.return_value,
            "play": mock_play,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }

        self.mocks["account"].liked_songs_uri = (
            "spotify:user:dummy_id:collection"
        )

        await async_play_liked_songs(self.mocks["hass"], self.mocks["call"])

    def test_play_media_was_called(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()
