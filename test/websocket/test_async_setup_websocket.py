"""Module to test the async_setup_websocket function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.websocket import (
    async_setup_websocket,
    HomeAssistant,
)

TEST_MODULE = "custom_components.spotcast.websocket"


class TestHandlerRegistration(IsolatedAsyncioTestCase):

    @patch(
        f"{TEST_MODULE}.websocket_api.async_register_command",
        new_callable=MagicMock,
    )
    async def asyncSetUp(self, mock_register: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "register": mock_register,
        }

        await async_setup_websocket(self.mocks["hass"])

    def test_10_handlers_registered(self):
        self.assertEqual(self.mocks["register"].call_count, 10)
