"""Module to test the async_get_playback function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.websocket.player_handler import (
    async_get_playback,
    HomeAssistant,
    ActiveConnection,
    SpotifyAccount
)

TEST_MODULE = "custom_components.spotcast.websocket.player_handler"


class TestPlaybackRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_entry: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_playback_state = AsyncMock()
        self.mocks["account"].async_playback_state.return_value = {
            "hello": "world"
        }

        await async_get_playback(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/player",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {"hello": "world"},
            )
        except AssertionError:
            self.fail()


class TestAccountSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_playback_state = AsyncMock()
        self.mocks["account"].async_playback_state.return_value = {
            "hello": "world"
        }

        await async_get_playback(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/devices",
                "account": "12345",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {"hello": "world"}
            )
        except AssertionError:
            self.fail()
