"""Moduel to test the entity_from_target_selector function"""


from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.services.utils import (
    entity_from_target_selector,
    HomeAssistant,
    UnmanagedSelectionError,
    TooManyMediaPlayersError,
)

TEST_MODULE = "custom_components.spotcast.services.utils"


class TestEntityProvided(TestCase):

    def setUp(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)

        media_players = {
            "entity_id": [
                "media_player.foo"
            ]
        }

        self.result = entity_from_target_selector(
            self.mock_hass,
            media_players,
        )

    def test_proper_entity_id_returned(self):
        self.assertEqual(self.result, "media_player.foo")


class TestDeviceProvided(TestCase):

    @patch(f"{TEST_MODULE}.entity_from_device_id")
    def setUp(self, mock_device: MagicMock):
        self.mock_hass = MagicMock(spec=HomeAssistant)

        media_players = {
            "device_id": [
                "12345"
            ]
        }
        mock_device.return_value = "media_player.foo"

        self.result = entity_from_target_selector(
            self.mock_hass,
            media_players,
        )

    def test_proper_entity_id_returned(self):
        self.assertEqual(self.result, "media_player.foo")


class TestUnmanagedTarget(TestCase):

    def test_error_raised(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)

        media_players = {
            "label": [
                "foo"
            ]
        }

        with self.assertRaises(UnmanagedSelectionError):
            entity_from_target_selector(
                self.mock_hass,
                media_players,
            )


class TestTooManyMediaPlayers(TestCase):

    def test_multiple_device_of_same_type(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)

        media_players = {
            "entity_id": [
                "media_player.foo",
                "media_player.bar",
            ]
        }

        with self.assertRaises(TooManyMediaPlayersError):
            entity_from_target_selector(
                self.mock_hass,
                media_players,
            )

    def test_multiple_types_at_once(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)

        media_players = {
            "entity_id": [
                "media_player.foo",
            ],
            "device_id": [
                "12345",
            ]
        }

        with self.assertRaises(TooManyMediaPlayersError):
            entity_from_target_selector(
                self.mock_hass,
                media_players,
            )
