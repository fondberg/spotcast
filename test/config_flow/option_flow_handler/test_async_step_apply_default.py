"""Module to test the async_step_apply_default function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.config_flow.option_flow_handler import (
    SpotcastOptionsFlowHandler
)


class TestNotSettingDefault(IsolatedAsyncioTestCase):

    @patch.object(SpotcastOptionsFlowHandler, "async_create_entry")
    async def asyncSetUp(self, mock_create: MagicMock):

        self.mocks = {
            "entry": MagicMock(spec=ConfigEntry),
            "create": mock_create,
        }

        self.mocks["entry"].options = {}
        self.mocks["entry"].title = "Dummy Entry"
        self.flow_handler = SpotcastOptionsFlowHandler(self.mocks["entry"])
        await self.flow_handler.async_step_apply_default(
            {"set_default": False}
        )

    def test_skipping_modification(self):
        try:
            self.mocks["create"].assert_called_with(
                title="",
                data={},
            )
        except AssertionError:
            self.fail()


class TestAlreadyDefault(IsolatedAsyncioTestCase):

    @patch.object(SpotcastOptionsFlowHandler, "async_create_entry")
    async def asyncSetUp(self, mock_create: MagicMock):

        self.mocks = {
            "entry": MagicMock(spec=ConfigEntry),
            "create": mock_create,
        }

        self.mocks["entry"].options = {}
        self.mocks["entry"].title = "Dummy Entry"
        self.mocks["entry"].data = {
            "is_default": True
        }
        self.flow_handler = SpotcastOptionsFlowHandler(self.mocks["entry"])
        await self.flow_handler.async_step_apply_default(
            {"set_default": True}
        )

    def test_skipping_modification(self):
        try:
            self.mocks["create"].assert_called_with(
                title="",
                data={},
            )
        except AssertionError:
            self.fail()


class TestSettingDefault(IsolatedAsyncioTestCase):

    @patch.object(SpotcastOptionsFlowHandler, "hass", spec=HomeAssistant)
    @patch.object(SpotcastOptionsFlowHandler, "async_create_entry")
    async def asyncSetUp(self, mock_create: MagicMock, mock_hass: MagicMock):

        self.mocks = {
            "entry": MagicMock(spec=ConfigEntry),
            "create": mock_create,
            "hass": mock_hass,
            "additional": MagicMock(spec=ConfigEntry),
            "non_default": MagicMock(spec=ConfigEntry),
            "additional_account": MagicMock(spec=SpotifyAccount),
            "non_default_account": MagicMock(spec=SpotifyAccount),
            "account": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["additional_account"].is_default = True
        self.mocks["non_default_account"].is_default = False
        self.mocks["account"].is_default = False

        self.mocks["entry"].options = {}
        self.mocks["entry"].title = "Dummy Entry"
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].data = {
            "is_default": False
        }
        self.mocks["additional"].title = "Additional Entry"
        self.mocks["additional"].entry_id = "67890"
        self.mocks["additional"].data = {
            "is_default": True
        }
        self.mocks["non_default"].title = "Non Default Entry"
        self.mocks["non_default"].entry_id = "1465"
        self.mocks["non_default"].data = {
            "is_default": False
        }

        self.mocks["hass"].config_entries.async_entries.return_value = [
            self.mocks["entry"],
            self.mocks["additional"],
            self.mocks["non_default"]
        ]

        self.mocks["hass"].data = {
            "spotcast": {
                "67890": self.mocks["additional_account"],
                "12345": self.mocks["account"],
                "1465": self.mocks["non_default_account"],
            }
        }

        self.flow_handler = SpotcastOptionsFlowHandler(self.mocks["entry"])

        await self.flow_handler.async_step_apply_default(
            {"set_default": True}
        )

    def test_entry_is_now_default(self):
        self.assertTrue(self.mocks["account"].is_default)

    def test_additional_is_not_default(self):
        self.assertFalse(self.mocks["additional_account"].is_default)
