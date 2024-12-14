"""Module to test the set_base_refresh_rate function"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.config_flow import (
    SpotcastOptionsFlowHandler,
)


class TestSettingRefreshRate(TestCase):

    def setUp(self):

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
        self.handler._options = self.mocks["entry"].options
        self.handler.hass = self.mocks["hass"]
        self.handler.set_base_refresh_rate(15)

    def test_account_refresh_rate_modified(self):
        self.assertEqual(self. mocks["account"].base_refresh_rate, 15)

    def test_entry_refresh_rate_modified(self):
        self.assertEqual(self. mocks["entry"].options["base_refresh_rate"], 15)


class TestSameRefreshRate(TestCase):

    def setUp(self):

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
        self.handler._options = self.mocks["entry"].options
        self.handler.hass = self.mocks["hass"]
        self.handler.set_base_refresh_rate(30)

    def test_account_refresh_rate_modified(self):
        self.assertEqual(self. mocks["account"].base_refresh_rate, 30)

    def test_entry_refresh_rate_modified(self):
        self.assertEqual(self. mocks["entry"].options["base_refresh_rate"], 30)
