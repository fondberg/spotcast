"""Module to test the definitions of the SERVICE dictionary"""

from unittest import TestCase
from voluptuous import Schema

from custom_components.spotcast.services.const import (
    SERVICE_SCHEMAS,
    SERVICE_HANDLERS,
)


def dummy_function():
    pass


class TestServiceSchemas(TestCase):

    def test_all_keys_are_strings(self):
        for key in SERVICE_SCHEMAS.keys():
            self.assertIsInstance(key, str)

    def test_all_schemas_are_volumptuous_schemas(self):
        for value in SERVICE_SCHEMAS.values():
            self.assertIsInstance(value, Schema)


class TestHandlers(TestCase):

    CALLABLE_TYPE = type(dummy_function)

    def test_all_keys_are_strings(self):
        for key in SERVICE_HANDLERS.keys():
            self.assertIsInstance(key, str)

    def test_all_handlers_are_callable(self):
        for value in SERVICE_HANDLERS.values():
            self.assertIsInstance(value, self.CALLABLE_TYPE)
