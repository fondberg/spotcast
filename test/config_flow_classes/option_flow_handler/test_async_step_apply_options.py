"""Module to test the async_step_apply_options function"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.config_flow_classes.options_flow_handler \
    import SpotcastOptionsFlowHandler


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
        self.mocks["hass"].config_entries.async_get_known_entry = MagicMock(
            return_value=self.mocks["entry"]
        )
        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"]
                }
            }
        }

        self.handler = SpotcastOptionsFlowHandler()
        self.handler._options = None
        self.handler.handler = "foo"
        self.handler.hass = self.mocks["hass"]
        self.handler.set_base_refresh_rate = MagicMock()
        self.handler.set_default_user = MagicMock()

        await self.handler.async_step_apply_options({
            "set_default": True,
            "base_refresh_rate": 30
        })

    def test_set_default_was_called(self):
        try:
            self.handler.set_default_user.assert_called_once()
        except AssertionError:
            self.fail()

    def test_set_base_refresh_rate_was_called(self):
        try:
            self.handler.set_base_refresh_rate.assert_called_once_with(30)
        except AssertionError:
            self.fail()


class TestWithoutDefaultSet(IsolatedAsyncioTestCase):

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

        self.mocks["hass"].config_entries.async_get_known_entry = MagicMock(
            return_value=self.mocks["entry"]
        )
        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"]
                }
            }
        }

        self.handler = SpotcastOptionsFlowHandler()
        self.handler._options = None
        self.handler.hass = self.mocks["hass"]
        self.handler.handler = "foo"
        self.handler.set_base_refresh_rate = MagicMock()
        self.handler.set_default_user = MagicMock()

        await self.handler.async_step_apply_options({
            "set_default": False,
            "base_refresh_rate": 30
        })

    def test_set_default_was_called(self):
        try:
            self.handler.set_default_user.assert_not_called()
        except AssertionError:
            self.fail()

    def test_set_base_refresh_rate_was_called(self):
        try:
            self.handler.set_base_refresh_rate.assert_called_once_with(30)
        except AssertionError:
            self.fail()
