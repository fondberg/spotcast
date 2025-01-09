"""Module to test the clean_device_type method"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.media_player.device_manager import (
    DeviceManager,
    SpotifyAccount,
    AddEntitiesCallback,
)


class TestStandardType(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "callback": MagicMock(spec=AddEntitiesCallback),
        }

        self.manager = DeviceManager(
            self.mocks["account"],
            self.mocks["callback"],
        )

        self.result = self.manager.clean_device_type({
            "name": "Dummy Device",
            "type": "Speaker",
            "id": "foo"
        })

    def test_device_type_unchanged(self):
        self.assertEqual(self.result, "Speaker")


class TestWebPlayer(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "callback": MagicMock(spec=AddEntitiesCallback),
        }

        self.manager = DeviceManager(
            self.mocks["account"],
            self.mocks["callback"],
        )

        self.result = self.manager.clean_device_type({
            "name": "Web Player - Dummy Browser",
            "type": "Speaker",
            "id": "foo"
        })

    def test_device_type_unchanged(self):
        self.assertEqual(self.result, "Web Player")


class TestEchoDevice(TestCase):

    def setUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "callback": MagicMock(spec=AddEntitiesCallback),
        }

        self.manager = DeviceManager(
            self.mocks["account"],
            self.mocks["callback"],
        )

        self.result = self.manager.clean_device_type({
            "name": "Dummy Speaker",
            "type": "Speaker",
            "id": "1234567890_amzn_2"
        })

    def test_device_type_unchanged(self):
        self.assertEqual(self.result, "Echo Speaker")
