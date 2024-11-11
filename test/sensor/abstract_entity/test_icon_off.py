"""Module to test the icon_off property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    SpotifyAccount,
)


class EntityWithoutOffIcon(SpotcastEntity):

    PLATFORM = "dummy"

    @property
    def icon(self):
        ...

    async def async_update(self):
        ...


class EntityWithOffIcon(EntityWithoutOffIcon):
    ICON_OFF = "mdi:overwrite"


class TestIconDefinition(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.entities = {
            "with": EntityWithOffIcon(self.mocks["account"]),
            "without": EntityWithoutOffIcon(self.mocks["account"]),
        }

    def test_entity_without_off_icon_returns_icon_with_off_added(self):
        self.assertEqual(self.entities["without"]._icon_off, "mdi:cube-off")

    def test_entity_with_off_icon_returns_overwritten_value(self):
        self.assertEqual(self.entities["with"]._icon_off, "mdi:overwrite")
