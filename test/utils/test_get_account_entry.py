"""Module to test the utility function get_account_entry"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.utils import (
    get_account_entry,
    HomeAssistant,
    ConfigEntry,
    AccountNotFoundError,
    NoDefaultAccountError,
)


class TestSpecificAccount(TestCase):

    def setUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.mock_hass.config_entries.async_get_entry\
            .return_value = self.mock_entry

        self.entry = get_account_entry(self.mock_hass, "foo")

    def test_entry_is_expected_entry(self):
        self.assertIs(self.entry, self.mock_entry)


class TestMissingAccount(TestCase):

    def test_missing_specifc_account(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.mock_hass.config_entries.async_get_entry\
            .return_value = None

        with self.assertRaises(AccountNotFoundError):
            get_account_entry(self.mock_hass, "foo")

    def test_no_default_account(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.mock_entry.data = {
            "is_default": False
        }
        self.mock_hass.config_entries.async_entries.return_value = [
            self.mock_entry,
        ]

        with self.assertRaises(NoDefaultAccountError):
            self.entry = get_account_entry(self.mock_hass)


class TestDefaultAccount(TestCase):

    def test_proper_error_raised(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.mock_entry.data = {
            "is_default": True
        }
        self.mock_hass.config_entries.async_entries.return_value = [
            self.mock_entry,
        ]

        self.entry = get_account_entry(self.mock_hass)

        self.assertIs(self.entry, self.mock_entry)
