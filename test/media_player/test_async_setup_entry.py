"""Module to test the async_setup_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.media_player import (
    async_setup_entry,
    SpotifyAccount,
    HomeAssistant,
    ConfigEntry,
    AddEntitiesCallback,
    DeviceManager,
)

TEST_MODULE = "custom_components.spotcast.media_player"


class TestMediaPlayerSetup(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_time_interval")
    @patch.object(DeviceManager, "async_update", new_callable=AsyncMock)
    @patch.object(
        SpotifyAccount,
        "async_from_config_entry",
        new_callable=AsyncMock,
        return_value=MagicMock(spec=SpotifyAccount)
    )
    async def asyncSetUp(
        self,
        mock_account: MagicMock,
        mock_update: MagicMock,
        mock_track_time: MagicMock,
    ):

        self.mock_update = mock_update
        self.mock_track_time = mock_track_time

        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_entry = MagicMock(spec=ConfigEntry)
        self.mock_callback = MagicMock(spec=AddEntitiesCallback)

        await async_setup_entry(
            self.mock_hass,
            self.mock_entry,
            self.mock_callback,
        )

    async def test_update_called(self):
        try:
            self.mock_update.assert_called()
        except AssertionError:
            self.fail()

    async def test_async_track_time_called_properly(self):
        try:
            self.mock_track_time.assert_called()
        except AssertionError:
            self.fail()
