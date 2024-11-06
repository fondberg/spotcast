"""Module to test async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_media import (
    async_play_media,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_media"


class TestBaseMediaPlayback(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.get_account_entry")
    async def asyncSetUp(self, mock_entry: MagicMock, mock_account: MagicMock):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry.return_value,
            "account": mock_account.return_value,
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "extras": {
                "volume": 80
            }
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_test(self):
        ...
