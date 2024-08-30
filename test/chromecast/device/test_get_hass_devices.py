"""Module to test the get_hass_devices function"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
import datetime as dt

from homeassistant.helpers.entity_platform import EntityPlatform

from custom_components.spotcast.chromecast.device import (
    ChromecastDevice,
    CastDevice,
)

MODULE_ROOT = "custom_components.spotcast.chromecast.device"


class TestHassDevices(TestCase):

    @patch(MODULE_ROOT+".extract_media_players")
    @patch(MODULE_ROOT+".entity_platform.async_get_platforms")
    def test_non_media_player_domain(
            self,
            mock_platforms: MagicMock,
            mock_players: MagicMock
    ):

        mock_platforms.return_value = [
            EntityPlatform(
                hass=MagicMock(),
                logger=MagicMock(),
                domain="Light",
                platform_name="kasa",
                platform=MagicMock(),
                scan_interval=dt.timedelta(seconds=60),
                entity_namespace=None
            )
        ]

        results = ChromecastDevice.get_hass_devices(MagicMock())

        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 0)

        try:
            mock_players.assert_not_called()
        except AssertionError:
            self.fail(
                "Extract Media Player was called on a non media player "
                "platform"
            )

    @patch(MODULE_ROOT+".extract_media_players")
    @patch(MODULE_ROOT+".entity_platform.async_get_platforms")
    def test_media_player_domain(
            self,
            mock_platforms: MagicMock,
            mock_players: MagicMock
    ):

        mock_platforms.return_value = [
            EntityPlatform(
                hass=MagicMock(),
                logger=MagicMock(),
                domain="media_player",
                platform_name="cast",
                platform=MagicMock(),
                scan_interval=dt.timedelta(seconds=60),
                entity_namespace=None
            )
        ]

        media_player = CastDevice(MagicMock(), MagicMock())
        media_player._name = "Mock Player"

        mock_players.return_value = {
            "media_player.mock_player": media_player
        }

        results = ChromecastDevice.get_hass_devices(MagicMock())

        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 1)

    @patch(MODULE_ROOT+".extract_media_players")
    @patch(MODULE_ROOT+".entity_platform.async_get_platforms")
    def test_keyed_by_id(
            self,
            mock_platforms: MagicMock,
            mock_players: MagicMock
    ):

        mock_platforms.return_value = [
            EntityPlatform(
                hass=MagicMock(),
                logger=MagicMock(),
                domain="media_player",
                platform_name="cast",
                platform=MagicMock(),
                scan_interval=dt.timedelta(seconds=60),
                entity_namespace=None
            )
        ]

        media_player = CastDevice(MagicMock(), MagicMock())
        media_player._name = "Mock Player"

        mock_players.return_value = {
            "media_player.mock_player": media_player
        }

        results = ChromecastDevice.get_hass_devices(MagicMock())

        self.assertIn("media_player.mock_player", results)

    @patch(MODULE_ROOT+".extract_media_players")
    @patch(MODULE_ROOT+".entity_platform.async_get_platforms")
    def test_keyed_by_name(
            self,
            mock_platforms: MagicMock,
            mock_players: MagicMock
    ):

        mock_platforms.return_value = [
            EntityPlatform(
                hass=MagicMock(),
                logger=MagicMock(),
                domain="media_player",
                platform_name="cast",
                platform=MagicMock(),
                scan_interval=dt.timedelta(seconds=60),
                entity_namespace=None
            )
        ]

        media_player = CastDevice(MagicMock(), MagicMock())
        media_player._name = "Mock Player"

        mock_players.return_value = {
            "media_player.mock_player": media_player
        }

        results = ChromecastDevice.get_hass_devices(
            MagicMock(),
            by_device_name=True
        )

        self.assertIn("Mock Player", results)
