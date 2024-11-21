"""Module to test the async_step_import function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.spotcast.config_flow.config_flow_handler import (
    SpotcastFlowHandler
)


class TestConfigImport(IsolatedAsyncioTestCase):

    @patch.object(SpotcastFlowHandler, "async_step_user")
    async def asyncSetUp(self, mock_user: AsyncMock):

        self.yaml_config = {
            "sp_dc": "foo",
            "sp_key": "bar",
            "accounts": {
                "foo": {
                    "sp_dc": "12345",
                    "sp_key": "34567"
                }
            }
        }

        self.mock_user = mock_user

        self.handler = SpotcastFlowHandler()
        await self.handler.async_step_import(self.yaml_config)

    def test_async_step_user_called_with_empty_input(self):
        try:
            self.mock_user.assert_called_with(None)
        except AssertionError:
            self.fail()

    def test_expected_values_from_yaml_config_saved(self):
        self.assertEqual(
            self.handler._import_data,
            {"sp_dc": "foo", "sp_key": "bar"}
        )
