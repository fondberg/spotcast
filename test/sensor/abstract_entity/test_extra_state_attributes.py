"""Module to test the extra_state_attributes property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    SpotifyAccount,
)


class DummyEntity(SpotcastEntity):
    PLATFORM = "dummy"
    DEFAULT_ATTRIBUTES = {"foo": []}

    @property
    def icon(self):
        ...

    async def async_update(self):
        ...


class TestExtraAttributes(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.entity = DummyEntity(self.account)

    def test_with_extra_attributes(self):
        self.assertEqual(self.entity.extra_state_attributes, {"foo": []})

    def test_without_extra_attributes(self):
        self.entity._attributes = None
        self.assertIsNone(self.entity.extra_state_attributes)
