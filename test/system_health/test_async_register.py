"""Module to test the async_register function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.system_health import (
    async_register,
    system_health_info,
    HomeAssistant,
    SystemHealthRegistration,
)


class TestRegisteringProperFunction(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "register": MagicMock(spec=SystemHealthRegistration),
        }

        async_register(self.mocks["hass"], self.mocks["register"])

    def test_register_called_with_expected_function(self):
        try:
            self.mocks["register"].async_register_info.assert_called_once_with(
                system_health_info
            )
        except AssertionError:
            self.fail()
