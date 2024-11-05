"""Module to test the entities_from_integration function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from homeassistant.helpers.entity_platform import EntityPlatform

from custom_components.spotcast.media_player.utils import (
    entities_from_integration,
    HomeAssistant
)

TEST_MODULE = "custom_components.spotcast.media_player.utils"


class TestNoFilter(TestCase):

    @patch(f"{TEST_MODULE}.async_get_platforms")
    def setUp(self, mock_platforms: MagicMock):

        mock_platform = MagicMock(spec=EntityPlatform)
        mock_platform.entities = {
            "media_player.foo": "foo",
            "media_player.bar": "bar"
        }

        mock_platform.domain = "media_player"
        mock_platform.platform_name = "foo"

        mock_platforms.return_value = [
            mock_platform
        ]

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.result = entities_from_integration(
            self.mock_hass,
            "spotcast"
        )

    def test_received_2_devices(self):
        self.assertEqual(len(self.result), 2)


class TestWithFilter(TestCase):

    @patch(f"{TEST_MODULE}.async_get_platforms")
    def setUp(self, mock_platforms: MagicMock):

        mock_platform = MagicMock(spec=EntityPlatform)
        mock_platform.entities = {
            "media_player.foo": "foo",
            "media_player.bar": "bar"
        }

        mock_platform.domain = "media_player"
        mock_platform.platform_name = "foo"

        mock_platforms.return_value = [
            mock_platform
        ]

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.result = entities_from_integration(
            self.mock_hass,
            "spotcast",
            "light"
        )

    def test_received_2_devices(self):
        self.assertEqual(len(self.result), 0)
