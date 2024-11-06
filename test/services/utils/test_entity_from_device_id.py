"""Module to test the entity_from_device_id function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.entity_registry import RegistryEntry

from custom_components.spotcast.services.utils import (
    entity_from_device_id,
    HomeAssistant,
    AmbiguousDeviceIdError,
    DeviceNotFoundError,
)

TEST_MODULE = "custom_components.spotcast.services.utils"


class TestEntityFromDevice(TestCase):

    @patch(f"{TEST_MODULE}.er.async_get")
    def setUp(self, mock_registry: MagicMock):

        self.mock_registry = mock_registry.return_value

        self.mock_devices = [
            MagicMock(spec=RegistryEntry),
            MagicMock(spec=RegistryEntry),
        ]

        for device, domain, entity_id in zip(
                self.mock_devices,
                ("sensor", "media_player"),
                ("sensor.foo", "media_player.bar")
        ):
            device.domain = domain
            device.entity_id = entity_id

        self.mock_registry.entities.get_entries_for_device_id\
            .return_value = self.mock_devices

        mock_hass = MagicMock(spec=HomeAssistant)

        self.result = entity_from_device_id(mock_hass, "12345")

    def test_correct_entity_returned(self):
        self.assertEqual(self.result, "media_player.bar")


class TestCustomDomain(TestCase):

    @patch(f"{TEST_MODULE}.er.async_get")
    def setUp(self, mock_registry: MagicMock):

        self.mock_registry = mock_registry.return_value

        self.mock_devices = [
            MagicMock(spec=RegistryEntry),
            MagicMock(spec=RegistryEntry),
        ]

        for device, domain, entity_id in zip(
                self.mock_devices,
                ("sensor", "media_player"),
                ("sensor.foo", "media_player.bar")
        ):
            device.domain = domain
            device.entity_id = entity_id

        self.mock_registry.entities.get_entries_for_device_id\
            .return_value = self.mock_devices

        mock_hass = MagicMock(spec=HomeAssistant)

        self.result = entity_from_device_id(mock_hass, "12345", "sensor")

    def test_correct_entity_returned(self):
        self.assertEqual(self.result, "sensor.foo")


class TestAmbiguousDevice(TestCase):

    @patch(f"{TEST_MODULE}.er.async_get")
    def test_raises_error(self, mock_registry: MagicMock):

        self.mock_registry = mock_registry.return_value

        self.mock_devices = [
            MagicMock(spec=RegistryEntry),
            MagicMock(spec=RegistryEntry),
        ]

        for device, domain, entity_id in zip(
                self.mock_devices,
                ("media_player", "media_player"),
                ("media_player.foo", "media_player.bar")
        ):
            device.domain = domain
            device.entity_id = entity_id

        self.mock_registry.entities.get_entries_for_device_id\
            .return_value = self.mock_devices

        mock_hass = MagicMock(spec=HomeAssistant)

        with self.assertRaises(AmbiguousDeviceIdError):
            entity_from_device_id(mock_hass, "12345")


class TestNoEntityOfDomainInDevice(TestCase):

    @patch(f"{TEST_MODULE}.er.async_get")
    def test_raises_error(self, mock_registry: MagicMock):

        self.mock_registry = mock_registry.return_value

        self.mock_devices = [
            MagicMock(spec=RegistryEntry),
            MagicMock(spec=RegistryEntry),
        ]

        for device, domain, entity_id in zip(
                self.mock_devices,
                ("media_player", "media_player"),
                ("media_player.foo", "media_player.bar")
        ):
            device.domain = domain
            device.entity_id = entity_id

        self.mock_registry.entities.get_entries_for_device_id\
            .return_value = self.mock_devices

        mock_hass = MagicMock(spec=HomeAssistant)

        with self.assertRaises(DeviceNotFoundError):
            entity_from_device_id(mock_hass, "12345", "sensor")
