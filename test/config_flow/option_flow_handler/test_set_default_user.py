"""Module to test the set_default_user function"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.config_flow.option_flow_handler import (
    SpotcastOptionsFlowHandler
)
from custom_components.spotcast.spotify.account import SpotifyAccount


class TestUserSwitchToDefault(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "other_entry": MagicMock(spec=ConfigEntry),
            "third_entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].data = {
            "external_api": "foo",
            "internal_api": "bar",
        }
        self.mocks["entry"].entry_id = "12345"
        self.mocks["entry"].title = "Dummy Name"
        self.mocks["entry"]._options = {
            "is_default": False,
            "base_refresh_rate": 30,
        }
        self.mocks["entry"].options = self.mocks["entry"]._options

        self.mocks["other_entry"].data = {
            "external_api": "foo",
            "internal_api": "bar",
        }
        self.mocks["other_entry"].entry_id = "23456"
        self.mocks["other_entry"].title = "Other Name"
        self.mocks["other_entry"]._options = {
            "is_default": True,
            "base_refresh_rate": 30,
        }
        self.mocks["other_entry"].options = self.mocks["other_entry"]._options

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": MagicMock(spec=SpotifyAccount)
                },
                "23456": {
                    "account": MagicMock(spec=SpotifyAccount)
                },
                "34567": {
                    "account": MagicMock(spec=SpotifyAccount)
                }
            }
        }

        self.mocks["third_entry"].data = {
            "external_api": "foo",
            "internal_api": "bar",
        }
        self.mocks["third_entry"].entry_id = "34567"
        self.mocks["third_entry"].title = "Third Name"
        self.mocks["third_entry"]._options = {
            "is_default": False,
            "base_refresh_rate": 30,
        }
        self.mocks["third_entry"].options = self.mocks["third_entry"]._options

        self.mocks["hass"].data["spotcast"]["12345"]["account"]\
            .is_default = True
        self.mocks["hass"].data["spotcast"]["23456"]["account"]\
            .is_default = False

        self.mocks["hass"].config_entries.async_entries.return_value = [
            self.mocks["entry"],
            self.mocks["other_entry"],
            self.mocks["third_entry"],
        ]

        self.handler = SpotcastOptionsFlowHandler()
        self.handler.config_entry = self.mocks["entry"]
        self.handler._options = None
        self.handler._options = self.mocks["entry"].options
        self.handler.hass = self.mocks["hass"]

        self.handler.set_default_user()

    def test_current_entry_set_to_default(self):
        self.assertTrue(self.mocks["entry"].options["is_default"])

    def test_other_entry_removed_from_default(self):
        try:
            self.mocks["hass"].config_entries.async_update_entry\
                .assert_any_call(
                    self.mocks["other_entry"],
                    options={"is_default": False, "base_refresh_rate": 30}
            )
        except AssertionError:
            self.fail()

    def test_current_account_set_to_default(self):
        self.assertTrue(
            self.mocks["hass"].data["spotcast"]["12345"]["account"].is_default
        )

    def test_other_account_set_to_default(self):
        self.assertFalse(
            self.mocks["hass"].data["spotcast"]["23456"]["account"].is_default
        )
