"""Module to test the async_unload_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast import (
    async_unload_entry,
    HomeAssistant,
    ConfigEntry,
    SERVICE_SCHEMAS
)


class TestFullUnloading(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": MagicMock(spec=SpotifyAccount),
            "listener": MagicMock(),
        }

        self.mocks["entry"].entry_id = "12345"
        self.mocks["hass"].config_entries.async_unload_platforms = AsyncMock()
        self.mocks["hass"].config_entries.async_unload_platforms\
            .return_value = True

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"],
                    "device_listener": self.mocks["listener"],
                }
            }
        }
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_remove = MagicMock()

        self.result = await async_unload_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_unload_ok_returned(self):
        self.assertTrue(self.result)

    def test_hass_data_was_cleaned(self):
        self.assertNotIn("12345", self.mocks["hass"].data["spotcast"])

    def test_listener_was_called_to_stop(self):
        try:
            self.mocks["listener"].assert_called()
        except AssertionError:
            self.fail()

    def test_all_services_unloaded(self):
        for service in SERVICE_SCHEMAS:
            try:
                self.mocks["hass"].services.async_remove.assert_any_call(
                    "spotcast",
                    service
                )
            except AssertionError:
                self.fail()


class TestNotLastUnloading(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": MagicMock(spec=SpotifyAccount),
            "listener": MagicMock(),
        }

        self.mocks["entry"].entry_id = "12345"
        self.mocks["hass"].config_entries.async_unload_platforms = AsyncMock()
        self.mocks["hass"].config_entries.async_unload_platforms\
            .return_value = True

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"],
                    "device_listener": self.mocks["listener"],
                },
                "23456": {
                    "account": MagicMock(spec=SpotifyAccount),
                    "device_listener": MagicMock(),
                }
            }
        }
        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_remove = MagicMock()

        self.result = await async_unload_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_unload_ok_returned(self):
        self.assertTrue(self.result)

    def test_hass_data_was_cleaned(self):
        self.assertNotIn("12345", self.mocks["hass"].data["spotcast"])

    def test_listener_was_called_to_stop(self):
        try:
            self.mocks["listener"].assert_called()
        except AssertionError:
            self.fail()

    def test_all_services_unloaded(self):
        try:
            self.mocks["hass"].services.async_remove.assert_not_called()
        except AssertionError:
            self.fail()


class TestFailedUnloading(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": MagicMock(spec=SpotifyAccount),
            "listener": MagicMock(),
        }

        self.mocks["entry"].entry_id = "12345"
        self.mocks["hass"].config_entries.async_unload_platforms = AsyncMock()
        self.mocks["hass"].config_entries.async_unload_platforms\
            .return_value = False

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"],
                    "device_listener": self.mocks["listener"],
                }
            }
        }

        self.result = await async_unload_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_unload_ok_returned(self):
        self.assertFalse(self.result)


class TestNoListener(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "account": MagicMock(spec=SpotifyAccount),
            "listener": MagicMock(),
        }

        self.mocks["entry"].entry_id = "12345"
        self.mocks["hass"].config_entries.async_unload_platforms = AsyncMock()
        self.mocks["hass"].config_entries.async_unload_platforms\
            .return_value = True

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account"],
                    "device_listener": None,
                }
            }
        }

        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_remove = MagicMock()

        self.result = await async_unload_entry(
            self.mocks["hass"],
            self.mocks["entry"],
        )

    def test_unload_ok_returned(self):
        self.assertTrue(self.result)

    def test_listener_was_not_called_to_stop(self):
        try:
            self.mocks["listener"].assert_not_called()
        except AssertionError:
            self.fail()
