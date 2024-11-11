"""Module to test the is_on property"""

from unittest import TestCase
from unittest.mock import MagicMock

from homeassistant.const import STATE_UNKNOWN, STATE_ON, STATE_OFF

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.binary_sensor.abstract_binary_sensor import (
    SpotcastBinarySensor
)


class DummySensor(SpotcastBinarySensor):
    async def async_update(self):
        ...


class TestIsOn(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)
        self.sensor._attr_state = STATE_ON

    def test_is_on(self):
        self.assertTrue(self.sensor.is_on)


class TestIsOff(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)
        self.sensor._attr_state = STATE_OFF

    def test_is_on(self):
        self.assertFalse(self.sensor.is_on)


class TestIsUnknown(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.sensor = DummySensor(self.account)
        self.sensor._attr_state = STATE_UNKNOWN

    def test_is_on(self):
        self.assertIsNone(self.sensor.is_on)
