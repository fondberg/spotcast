"""Module to test the async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.play_media import (
    async_play_media,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
    Chromecast,
    SpotifyController,
)

TEST_MODULE = "custom_components.spotcast.services.play_media"


class TestMediaPlay(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.SpotifyController")
    @patch.object(Chromecast, "from_hass")
    @patch.object(
        SpotifyAccount,
        "async_from_config_entry",
        new_callable=AsyncMock
    )
    async def asyncSetUp(
            self,
            mock_account_getter: AsyncMock,
            mock_player_getter: MagicMock,
            mock_controller: MagicMock,
    ):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_call = MagicMock(spec=ServiceCall)
        mock_config = MagicMock(spec=ConfigEntry)
        mock_account = AsyncMock(spec=SpotifyAccount)
        mock_player = MagicMock()
        mock_account_getter.return_value = mock_account
        mock_player_getter.return_value = mock_player

        self.mock_play_media = AsyncMock()

        mock_account.async_play_media = self.mock_play_media

        mock_hass.async_add_executor_job = AsyncMock()
        mock_player.id = "12345"

        mock_hass.data = {
            "spotcast": {
                "dummy_account": mock_config
            }
        }

        mock_call.data = {
            "spotify_uri": "spotify:album:1oSxrt8srwdUqlg5jq3aFK",
            "account": "dummy_account",
            "entity_id": "media_player.living_room",
        }

        mock_player.register_handler.return_value = None

        await async_play_media(mock_hass, mock_call)

    def test_play_media_was_called_properly(self):
        try:
            self.mock_play_media.assert_called_with(
                "12345",
                "spotify:album:1oSxrt8srwdUqlg5jq3aFK"
            )
        except AssertionError:
            self.fail()
