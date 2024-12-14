"""Module to test the constructor of the SpotcastFlowHandler"""

from unittest import TestCase

from custom_components.spotcast.config_flow import (
    SpotcastFlowHandler
)


class TestConstruction(TestCase):

    def setUp(self):
        self.flow_handler = SpotcastFlowHandler()

    def test_data_attribute_initialised(self):
        try:
            self.flow_handler.data
        except AttributeError:
            self.fail("data was not intiatilsed")

    def test_data_is_dictionary(self):
        self.assertIsInstance(self.flow_handler.data, dict)
