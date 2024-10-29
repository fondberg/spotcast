"""Module to test the constructor of the ServiceHandler object"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.services.service_handler import (
    ServiceHandler,
    HomeAssistant,
)


class TestDataretention(TestCase):

    def setUp(self):
        self.hass = MagicMock(spec=HomeAssistant)
        self.handler = ServiceHandler(self.hass)

    def test_hass_object_retained(self):
        self.assertIs(self.handler.hass, self.hass)
