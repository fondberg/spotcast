"""Module to test the async_transfer_playback"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.services.transfer_playback import (
    async_transfer_playback,
    HomeAssistant,
    ServiceCall,
)

TEST_MODULE = "custom_components.spotcast.services.transfer_playback"


class TestTransferOfPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(self, mock_play: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }

        await async_transfer_playback(self.mocks["hass"], self.mocks["call"])

    def test_call_dat_updated(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": None,
            }

        )

    def test_play_media_was_called(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()
