"""Module that test the service handler are properly defined"""

from unittest import TestCase

import voluptuous as vol

from custom_components.spotcast.services.const import (
    SERVICE_SCHEMAS,
    SERVICE_HANDLERS,
)


class TestSchemasToHandlersPresence(TestCase):

    def test_all_schemas_have_a_handler_to_go_with(self):
        for service in SERVICE_SCHEMAS:
            self.assertIn(service, SERVICE_HANDLERS)

    def test_all_handlers_have_a_schema_to_go_with(self):
        for service in SERVICE_HANDLERS:
            self.assertIn(service, SERVICE_SCHEMAS)


class TestSchemas(TestCase):

    def test_all_schemas_are_volumptuous_schemas(self):
        for schema in SERVICE_SCHEMAS.values():
            self.assertIsInstance(schema, vol.Schema)
