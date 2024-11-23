"""Module to test the async_step_reauth_confirm function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.config_flow.config_flow_handler import (
    SpotcastFlowHandler,
    ConfigEntry
)


class TestFirstCall(IsolatedAsyncioTestCase):

    @patch.object(SpotcastFlowHandler, "async_step_pick_implementation")
    @patch.object(SpotcastFlowHandler, "async_show_form", new_callable=MagicMock)
    @patch.object(SpotcastFlowHandler, "_get_reauth_entry", new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_entry: MagicMock,
            mock_form: MagicMock,
            mock_impl: AsyncMock
    ):

        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "entry": mock_entry.return_value,
            "form": mock_form,
            "implementation": mock_impl
        }

        self.mocks["entry"].data = {
            "external_api": {
                "id": "dummy_id"
            }
        }

        self.handler = SpotcastFlowHandler()

        await self.handler.async_step_reauth_confirm()

    def test_show_form_called(self):
        try:
            self.mocks["form"].assert_called_with(
                step_id="reauth_confirm",
                description_placeholders={
                    "account": "dummy_id"
                },
                errors={},
            )
        except AssertionError:
            self.fail()

    def test_pick_implementation_not_called(self):
        try:
            self.mocks["implementation"].assert_not_called()
        except AssertionError:
            self.fail()


class TestSecondtCall(IsolatedAsyncioTestCase):

    @patch.object(SpotcastFlowHandler, "async_step_pick_implementation")
    @patch.object(SpotcastFlowHandler, "async_show_form", new_callable=MagicMock)
    @patch.object(SpotcastFlowHandler, "_get_reauth_entry", new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_entry: MagicMock,
            mock_form: MagicMock,
            mock_impl: AsyncMock
    ):

        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "entry": mock_entry.return_value,
            "form": mock_form,
            "implementation": mock_impl
        }

        self.mocks["entry"].data = {
            "external_api": {
                "id": "dummy_id",
                "auth_implementation": "foo"
            }
        }

        self.handler = SpotcastFlowHandler()

        await self.handler.async_step_reauth_confirm({})

    def test_show_form_not_called(self):
        try:
            self.mocks["form"].assert_not_called()
        except AssertionError:
            self.fail()

    def test_pick_implementation_called(self):
        try:
            self.mocks["implementation"].assert_called_with(
                user_input={
                    "implementation": "foo"
                }
            )
        except AssertionError:
            self.fail()
