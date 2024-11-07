"""Module to test the async_play_dj function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_dj import (
    async_play_dj,
    HomeAssistant,
    ServiceCall,
)

TEST_MODULE = "custom_components.spotcast.services.play_dj"


class TestBaseMediaPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
        self,
        mock_play_media: MagicMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
        }

        self.mocks["call"].data = {
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "volume": 80
            }
        }
