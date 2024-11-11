"""Module to test the async_step_init function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.config_flow.option_flow_handler import (
    SpotcastOptionsFlowHandler,
)


class TestInitStep(IsolatedAsyncioTestCase):

    @patch.object(SpotcastOptionsFlowHandler, "async_show_form")
    async def asyncSetUp(self, mock_form: AsyncMock):
        self.entry = MagicMock(spec=ConfigEntry)
        self.show_form = mock_form
        self.entry.options = {}
        self.flow_handler = SpotcastOptionsFlowHandler(self.entry)
        await self.flow_handler.async_step_init()

    def test_init_form_was_shown(self):
        try:
            self.show_form.assert_called_with(
                step_id="apply_default",
                data_schema=self.flow_handler.SCHEMAS["init"],
                errors={},
                last_step=True,
            )
        except AssertionError:
            self.fail()
