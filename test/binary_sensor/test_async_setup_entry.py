"""Module to test the async_setup_entry"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.binary_sensor import (
    async_setup_entry,
    HomeAssistant,
    ConfigEntry,
    AddEntitiesCallback,
    SpotifyAccount,
)


class TestSetupEntry(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": mock_account.return_value,
            "add_entities": MagicMock(spec=AddEntitiesCallback),
        }

        await async_setup_entry(
            self.mocks["hass"],
            self.mocks["entry"],
            self.mocks["add_entities"],
        )

    def test_async_add_entities_was_called(self):
        try:
            self.mocks["add_entities"].assert_called()
        except AssertionError:
            self.fail()
