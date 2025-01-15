"""Module to test the async_get_options_flow method"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.config_flow_classes.config_flow_handler\
    import (
        SpotcastFlowHandler,
        ConfigEntry,
        SpotcastOptionsFlowHandler,
    )


class TestCreationOfOptionFlow(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.entry = MagicMock(spec=ConfigEntry)
        self.flow_handler = SpotcastFlowHandler()

        self.entry.options = {}

        self.option_flow_handler\
            = SpotcastFlowHandler.async_get_options_flow(self.entry)

    def test_object_returned_is_option_flow_handler(self):
        self.assertIsInstance(
            self.option_flow_handler,
            SpotcastOptionsFlowHandler,
        )
