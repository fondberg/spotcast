"""Module to test the async_step_import"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.config_flow import (
    SpotcastFlowHandler,
    vol,
)


class TestImportOfYAMLConfig(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "form": MagicMock(),
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.async_show_form = self.mocks["form"]
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_call = AsyncMock()

        self.result = await self.handler.async_step_import({
            "sp_dc": "foo",
            "sp_key": "bar",
        })

    def test_pick_implementation_form_called(self):
        try:
            self.mocks["form"].assert_called_with(
                step_id="pick_implementation",
                data_schema=vol.Schema({}),
            )
        except AssertionError:
            self.fail()

    def test_notification_service(self):
        try:
            self.mocks["hass"].services.async_call.assert_called()
        except AssertionError:
            self.fail()

    def test_data_from_yaml_saved(self):
        self.assertEqual(
            self.handler._import_data,
            {"sp_dc": "foo", "sp_key": "bar"}
        )
