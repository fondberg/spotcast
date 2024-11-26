"""Module to test the async_step_apply_options function"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.config_flow.option_flow_handler import (
    SpotcastOptionsFlowHandler,
)


class TestWithDefaultSet(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["entry"].data = {
            "external_api": "foo",
            "internal_api": "bar",
        }
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].title = "Dummy Name"
        self.mocks["entry"].options = {
            "is_default": True,
            "base_refresh_rate": 30,
        }

        self.mocks["account"].base_refresh_rate = 30

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"]
                }
            }
        }

        self.handler = SpotcastOptionsFlowHandler(self.mocks["entry"])
        self.handler._options = None
        self.handler.hass = self.mocks["hass"]
        self.handler.async_show_form = MagicMock()

        await self.handler.async_step_init({})

    def test_async_show_form_called_with_proper_args(self):
        try:
            self.handler.async_show_form.assert_called_with(
                step_id="apply_options",
                data_schema=self.handler.add_suggested_values_to_schema(
                    self.handler.SCHEMAS["init"],
                    {"is_default": True, "base_refresh_rate": 30},
                ),
                errors={},
            )
        except AssertionError:
            self.fail()
