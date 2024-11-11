"""Module to test the async_setup_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.sensor import (
    async_setup_entry,
    HomeAssistant,
    ConfigEntry,
    AddEntitiesCallback,
    SpotifyAccount
)

TEST_MODULE = "custom_components.spotcast.sensor"


class TestSensorCreation(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.SpotifyAccountTypeSensor")
    @patch(f"{TEST_MODULE}.SpotifyFollowersSensor")
    @patch(f"{TEST_MODULE}.SpotifyProductSensor")
    @patch(f"{TEST_MODULE}.SpotifyLikedSongsSensor")
    @patch(f"{TEST_MODULE}.SpotifyProfileSensor")
    @patch(f"{TEST_MODULE}.SpotifyPlaylistsSensor")
    @patch(f"{TEST_MODULE}.SpotifyDevicesSensor")
    async def asyncSetUp(
        self,
        mock_devices: MagicMock,
        mock_playlists: MagicMock,
        mock_profile: MagicMock,
        mock_liked_songs: MagicMock,
        mock_product: MagicMock,
        mock_followers: MagicMock,
        mock_account_type: MagicMock,
    ):

        self.mocks = {
            "devices": mock_devices,
            "playlists": mock_playlists,
            "profile": mock_profile,
            "liked_songs": mock_liked_songs,
            "product": mock_product,
            "followers": mock_followers,
            "account_type": mock_account_type,
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
            "add_entities": MagicMock(spec=AddEntitiesCallback),
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].id = "dummy_account"

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": self.mocks["account"]
            }
        }

        self.mocks["entry"].entry_id = "12345"

        await async_setup_entry(
            self.mocks["hass"],
            self.mocks["entry"],
            self.mocks["add_entities"]
        )

    def assert_sensor_was_created(self, mock_object: MagicMock):
        try:
            mock_object.assert_called()
        except AssertionError:
            self.fail()

    def test_add_entity_was_called(self):
        self.assert_sensor_was_created(self.mocks["add_entities"])
