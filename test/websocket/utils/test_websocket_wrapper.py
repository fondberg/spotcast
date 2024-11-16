"""Module to test the websocket wrapper"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.websocket.utils import (
    websocket_wrapper,
    HomeAssistant,
    ActiveConnection,
    ServiceValidationError,
)


@websocket_wrapper
async def working_function(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict,
):
    return "foo"


@websocket_wrapper
async def broken_function(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict,
):
    raise ServiceValidationError("test error")


class TestWorkingCall(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
        }

        self.result = await working_function(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1}
        )

    def test_expected_return_from_function(self):
        self.assertEqual(self.result, "foo")


class TestBrokenCall(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
        }

        self.result = await broken_function(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1}
        )

    def test_error_sent(self):
        try:
            self.mocks["connection"].send_error.assert_called_with(
                1,
                "ServiceValidationError",
                "test error",
            )
        except AssertionError:
            self.fail()
