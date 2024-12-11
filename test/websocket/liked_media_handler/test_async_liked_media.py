"""Module to test the async_liked_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.liked_media_handler import (
    async_liked_media,
    HomeAssistant,
    ActiveConnection,
)

from test.websocket.liked_media_handler import TEST_MODULE


class TestBasicLikedMediaRequest(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_liked_songs = AsyncMock(
            return_value=["foo", "bar", "baz"]
        )
        self.mocks["account"].id = "12345"

        await async_liked_media(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1},
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "tracks": ["foo", "bar", "baz"],
                }
            )
        except AssertionError:
            self.fail()
