"""Module ot test the async method step_internal_api"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.config_flow import SpotcastFlowHandler


class TestInternalApiSetup(IsolatedAsyncioTestCase):

    def setUp(self):

        self.external_api = {
            "auth_implementation": "spotcast_foo",
            "token": {
                "access_token": "12345",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refreh_token": "ABCDF",
                "expires_at": 1729807129.8667192
            }
        }

        self.internal_api = {
            "sp_dc": "foo",
            "sp_key": "bar"
        }

        self.flow_handler = SpotcastFlowHandler()
        self.flow_handler.data = {
            "external_api": self.external_api
        }

    @patch.object(SpotcastFlowHandler, "async_oauth_create_entry")
    async def test_integration_of_internal_api_information(
            self,
            mock_create: MagicMock
    ):

        await self.flow_handler.async_step_internal_api(self.internal_api)

        try:
            mock_create.assert_called_with({
                "external_api": self.external_api,
                "internal_api": self.internal_api,
            })
        except AssertionError:
            self.fail("The provided data was not the expected one")
