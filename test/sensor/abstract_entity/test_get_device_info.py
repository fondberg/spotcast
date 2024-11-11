"""Module to test the constructor of the Spotcast Entity Class"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    SpotifyAccount,
    EntityCategory,
)


class DummyDeviceFromAccount(SpotcastEntity):

    DEFAULT_ATTRIBUTES = {"foo": []}
    PLATFORM = "dummy"
    ENTITY_CATEGORY = EntityCategory.CONFIG

    @property
    def icon(self):
        """Unimplemented icon property"""

    async def async_update(self):
        """Unimplemented async_update"""


class DummyNoDevice(DummyDeviceFromAccount):
    DEVICE_SOURCE = None


class DummyBadDeviceSource(DummyDeviceFromAccount):
    DEVICE_SOURCE = "invalid"


class TestDeviceInfoFromAccount(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].id = "dummy_id"

        self.entity = DummyDeviceFromAccount(self.mocks["account"])

    def test_device_info_from_account(self):
        self.assertIs(
            self.entity.device_info,
            self.mocks["account"].device_info
        )


class TestDeviceInfoNone(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].id = "dummy_id"

        self.entity = DummyNoDevice(self.mocks["account"])

    def test_device_info_from_account(self):
        self.assertIsNone(self.entity.device_info)


class TestDeviceInfoBadSource(TestCase):

    def test_raises_error(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].id = "dummy_id"

        with self.assertRaises(ValueError):
            self.entity = DummyBadDeviceSource(self.mocks["account"])
