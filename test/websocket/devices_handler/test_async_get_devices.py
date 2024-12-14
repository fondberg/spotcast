"""Module to test the async_get_devices function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.devices_handler import (
    async_get_devices,
    HomeAssistant,
    ActiveConnection,
)

TEST_MODULE = "custom_components.spotcast.websocket.devices_handler"


class TestDevicesRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].id = "12345"
        self.mocks["account"].async_devices = AsyncMock(return_value=[
            "foo",
            "bar",
            "baz",
        ])

        await async_get_devices(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/devices",
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "devices": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()
