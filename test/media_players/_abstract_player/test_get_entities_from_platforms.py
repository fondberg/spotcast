"""Module to test the get_entities_from_platform method"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import EntityPlatform

from custom_components.spotcast.media_players._abstract_player import (
    MediaPlayer,
    MissingDeviceTypeError,
    InvalidPlatformError,
)


class MissingPlatformPlayer(MediaPlayer):
    DEVICE_TYPE = MagicMock


class MissingDeviceTypePlayer(MediaPlayer):
    PLATFORM = "mock"


class FullImplementationPlayer(MediaPlayer):
    PLATFORM = "mock"
    DEVICE_TYPE = MagicMock


class TestInvalidImplementation(TestCase):

    def test_missing_platform(self):
        with self.assertRaises(InvalidPlatformError):
            MissingPlatformPlayer._get_entities_from_platforms(MagicMock())

    def test_missing_device_type(self):
        with self.assertRaises(MissingDeviceTypeError):
            MissingDeviceTypePlayer._get_entities_from_platforms(MagicMock())


class TestEntityCrawling(TestCase):

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_no_platform_with_propoer_domain(self, mock_platforms: MagicMock):

        mock_platforms.return_value = [
            EntityPlatform(
                hass=MagicMock(),
                domain="mock",
                platform_name="light",
                logger=MagicMock(),
                scan_interval=dt.timedelta(seconds=60),
                platform=MagicMock(),
                entity_namespace=None,
            )
        ]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock()
        )

        self.assertEqual(len(result), 0)

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_single_platform(self, mock_platforms: MagicMock):

        platform = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        platform.entities = {
            "media_player.mock_player": MagicMock()
        }

        mock_platforms.return_value = [platform]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock()
        )

        self.assertEqual(len(result), 1)

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_multiple_platforms(self, mock_platforms: MagicMock):

        platform_a = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        platform_a.entities = {
            "media_player.mock_player_1": MagicMock()
        }

        platform_b = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        platform_b.entities = {
            "media_player.mock_player_2": MagicMock()
        }

        mock_platforms.return_value = [platform_a, platform_b]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock()
        )

        self.assertEqual(len(result), 2)

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_wrong_type_entity(self, mock_platforms: MagicMock):

        platform = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        platform.entities = {
            "media_player.mock_player": "invalid"
        }

        mock_platforms.return_value = [platform]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock()
        )

        self.assertEqual(len(result), 0)

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_default_provides_entity_id_as_key(
            self,
            mock_platforms: MagicMock
    ):

        platform = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        platform.entities = {
            "media_player.mock_player": MagicMock()
        }

        mock_platforms.return_value = [platform]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock()
        )

        self.assertEqual(len(result), 1)
        self.assertIn("media_player.mock_player", result)

    @patch(
        "custom_components.spotcast.media_players._abstract_player"
        ".async_get_platforms"
    )
    def test_provides_device_name_as_key_on_request(
            self,
            mock_platforms: MagicMock
    ):

        platform = EntityPlatform(
            hass=MagicMock(),
            domain="media_player",
            platform_name="mock",
            logger=MagicMock(),
            scan_interval=dt.timedelta(seconds=60),
            platform=MagicMock(),
            entity_namespace=None,
        )

        mock_player = MagicMock()
        mock_player.name = "Mock Player"

        platform.entities = {
            "media_player.mock_player": mock_player
        }

        mock_platforms.return_value = [platform]

        result = FullImplementationPlayer._get_entities_from_platforms(
            MagicMock(),
            by_device_name=True,
        )

        self.assertEqual(len(result), 1)
        self.assertIn("Mock Player", result)
