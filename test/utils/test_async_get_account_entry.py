"""Module to test the async_get_account_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.spotcast.utils import (
    async_get_account_entry,
    HomeAssistant,
    ConfigEntry,
    AccountNotFoundError,
    NoDefaultAccountError,
)


class TestAccountIdProvided(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)

        self.mock_hass.config_entries.async_get_entry = AsyncMock(
            return_value=self.mock_entry
        )

        self.result = await async_get_account_entry(self.mock_hass, "foo")

    def test_config_entry_returned(self):
        self.assertIs(self.result, self.mock_entry)


class TestNoneExistingEntry(IsolatedAsyncioTestCase):

    async def test_raises_error(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.mock_hass.config_entries.async_get_entry = AsyncMock(
            return_value=None
        )

        with self.assertRaises(AccountNotFoundError):
            await async_get_account_entry(self.mock_hass, "foo")


class TestNoAccountIdProvided(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.mock_entries = [MagicMock(spec=ConfigEntry) for _ in range(2)]

        for entry, is_default in zip(self.mock_entries, (False, True)):
            entry.data = {
                "is_default": is_default
            }

        self.mock_hass.config_entries.async_entries = AsyncMock(
            return_value=self.mock_entries
        )

        self.result = await async_get_account_entry(self.mock_hass)

    def test_config_entry_returned(self):
        self.assertIs(self.result, self.mock_entries[1])


class TestNoDefaultAccount(IsolatedAsyncioTestCase):

    async def test_raises_error(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.mock_entries = [MagicMock(spec=ConfigEntry) for _ in range(2)]

        for entry, is_default in zip(self.mock_entries, (False, False)):
            entry.data = {
                "is_default": is_default
            }

        self.mock_hass.config_entries.async_entries = AsyncMock(
            return_value=self.mock_entries
        )

        with self.assertRaises(NoDefaultAccountError):
            await async_get_account_entry(self.mock_hass)
