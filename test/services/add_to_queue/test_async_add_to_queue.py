"""Module to test the async_add_to_queue function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.add_to_queue import (
    async_add_to_queue,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
    NoActivePlaybackError,
)

TEST_MODULE = "custom_components.spotcast.services.add_to_queue"


class TestPlaybackActive(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_entry: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "entry": mock_entry.return_value
        }

        self.mocks["call"].data = {"spotify_uris": ["foo", "bar", "baz"]}
        self.mocks["account"].async_playback_state = AsyncMock()
        self.mocks["account"].async_playback_state.return_value = {
            "device": {
                "id": "12345"
            }
        }

        await async_add_to_queue(self.mocks["hass"], self.mocks["call"])

    def test_add_to_queue_was_call_for_all_uris(self):

        for uri in ("foo", "bar", "baz"):
            try:
                self.mocks["account"].async_add_to_queue.assert_any_call(uri)
            except AssertionError:
                self.fail()

    def test_addd_to_queue_called_three_times(self):
        self.assertEqual(
            self.mocks["account"].async_add_to_queue.call_count,
            3,
        )


class TestNoPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(self, mock_account: AsyncMock, mock_entry: MagicMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "entry": mock_entry.return_value
        }

        self.mocks["call"].data = {"spotify_uris": ["foo", "bar", "baz"]}
        self.mocks["account"].async_playback_state = AsyncMock()
        self.mocks["account"].async_playback_state.return_value = {}

        with self.assertRaises(NoActivePlaybackError):
            await async_add_to_queue(self.mocks["hass"], self.mocks["call"])

    def test_add_to_queue_was_never_called(self):

        for uri in ("foo", "bar", "baz"):
            try:
                self.mocks["account"].async_add_to_queue.assert_not_called()
            except AssertionError:
                self.fail()
