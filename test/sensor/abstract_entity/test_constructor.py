"""Module to test the constructor of the Spotcast Entity Class"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    SpotifyAccount,
    EntityCategory,
)


class DummyEntity(SpotcastEntity):

    DEFAULT_ATTRIBUTES = {"foo": []}
    PLATFORM = "dummy"
    ENTITY_CATEGORY = EntityCategory.CONFIG

    @property
    def icon(self):
        """Unimplemented icon property"""

    async def async_update(self):
        """Unimplemented async_update"""


class TestDataRetention(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].id = "dummy_id"

        self.entity = DummyEntity(self.mocks["account"])

    def test_account_is_retained(self):
        self.assertIs(self.entity.account, self.mocks["account"])

    def test_attributes_set_to_default(self):
        self.assertEqual(self.entity._attributes, {"foo": []})

    def test_entity_id_correctly_created(self):
        self.assertEqual(
            self.entity.entity_id,
            "dummy.dummy_id_abstract_spotcast"
        )

    def test_device_info_from_account_by_default(self):
        self.assertIs(
            self.entity._attr_device_info,
            self.mocks["account"].device_info
        )

    def test_entity_category_set_to_child_value(self):
        self.assertEqual(self.entity.entity_category, EntityCategory.CONFIG)
