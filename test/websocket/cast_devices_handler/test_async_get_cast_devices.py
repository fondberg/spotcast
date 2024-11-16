"""Moduel to test the async_get_cast_devices function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.websocket.cast_devices_handler import (
    async_get_cast_devices,
    HomeAssistant,
    ActiveConnection,
    CastDevice,
)

TEST_MODULE = "custom_components.spotcast.websocket.cast_devices_handler"


class TestCastDeviceRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_entities_from_integration")
    async def asyncSetUp(self, mock_entities: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "cast_device": MagicMock(spec=CastDevice),
            "mock_entities": mock_entities,
        }

        self.mocks["cast_device"]._cast_info = MagicMock()
        self.mocks["cast_device"]._cast_info.cast_info.uuid = "12345"
        self.mocks["cast_device"]._cast_info.cast_info.model_name = (
            "dummy player"
        )
        self.mocks["cast_device"]._cast_info.cast_info.friendly_name = (
            "Kitchen Speaker"
        )
        self.mocks["cast_device"]._cast_info.cast_info.manufacturer = "ACME"

        self.mocks["mock_entities"].return_value = {
            "media_player.kitchen_speaker": self.mocks["cast_device"]
        }

        await async_get_cast_devices(
            self.mocks["hass"],
            self.mocks["connection"],
            {
                "id": 1,
                "type": "spotcast/castdevices"
            }
        )

    def test_proper_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 1,
                    "devices": [
                        {
                            "entity_id": "media_player.kitchen_speaker",
                            "uuid": "12345",
                            "model_name": "dummy player",
                            "friendly_name": "Kitchen Speaker",
                            "manufacturer": "ACME",
                        }
                    ]
                }
            )
        except AssertionError:
            self.fail()
