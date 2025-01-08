"""Module to test the async_setup function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast import (
    async_setup,
    HomeAssistant,
    SOURCE_IMPORT,
)


class TestMissingDomainInConfig(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
        }

        self.result = await async_setup(
            self.mocks["hass"],
            {}
        )

    def test_returns_true(self):
        self.assertTrue(self.result)

    def test_create_task_not_called(self):
        try:
            self.mocks["hass"].async_create_task.assert_not_called()
        except AssertionError:
            self.fail()


class TestInvalidConfig(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
        }

        self.result = await async_setup(
            self.mocks["hass"],
            {"spotcast": {"sp_dc": "foo"}}
        )

    def test_returns_false(self):
        self.assertFalse(self.result)

    def test_create_task_not_called(self):
        try:
            self.mocks["hass"].async_create_task.assert_not_called()
        except AssertionError:
            self.fail()


class TestValidConfig(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
        }

        self.result = await async_setup(
            self.mocks["hass"],
            {"spotcast": {"sp_dc": "foo", "sp_key": "bar"}}
        )

    def test_returns_true(self):
        self.assertTrue(self.result)

    def test_create_task_called(self):
        try:
            self.mocks["hass"].async_create_task.assert_called()
        except AssertionError:
            self.fail()

    def test_config_init_called(self):
        try:
            self.mocks["hass"].config_entries.flow.async_init\
                .assert_called_with(
                    "spotcast",
                    context={"source": SOURCE_IMPORT},
                    data={"sp_dc": "foo", "sp_key": "bar"},
            )
        except AssertionError:
            self.fail()
