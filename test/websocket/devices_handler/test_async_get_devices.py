"""Module to test the async_get_devices function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.websocket.devices_handler import (
    async_get_devices,
    HomeAssistant,
    ActiveConnection,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.websocket.devices_handler"


class TestDevicesRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_entry: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
            "entry": mock_entry.return_value
        }

        self.mocks["entry"].entry_id = "12345"
        self.mocks["account"].async_devices = AsyncMock()
        self.mocks["account"].async_devices.return_value = [
            "foo",
            "bar",
            "baz",
        ]

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


class TestAccountSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.search_account", new_callable=MagicMock)
    async def asyncSetUp(self, mock_account: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_devices = AsyncMock()
        self.mocks["account"].async_devices.return_value = [
            "foo",
            "bar",
            "baz",
        ]

        await async_get_devices(
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
                {
                    "total": 3,
                    "account": "12345",
                    "devices": ["foo", "bar", "baz"]
                }
            )
        except AssertionError:
            self.fail()
