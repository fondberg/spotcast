"""Module to test the name property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    SpotifyAccount,
)


class DummyEntity(SpotcastEntity):
    PLATFORM = "dummy"

    @property
    def icon(self):
        ...

    async def async_update(self):
        ...


class TestNameDefinition(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.name = "Dummy Account"
        self.entity = DummyEntity(self.account)

    def test_name_value_is_as_expected(self):
        self.assertEqual(
            self.entity.name,
            "Spotcast - Dummy Account Abstract Spotcast"
        )
