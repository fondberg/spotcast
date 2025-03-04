"""Module to test the async_transfer_playback"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.transfer_playback import (
    async_transfer_playback,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
    ServiceValidationError,
)

from test.services.transfer_playback import TEST_MODULE


class TestTransferOfActivePlayback(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
            self,
            mock_play: AsyncMock,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
    ):
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
            "account": mock_account.return_value,
            "entry": mock_entry.return_value,
        }

        self.mocks["account"].async_playback_state = AsyncMock(
            return_value={
                "device": "foo",
                "context": "bar"
            }
        )

        self.mocks["account"].async_last_playback_state = AsyncMock()
        self.mocks["account"].async_last_playback_state.return_value = {}

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }

        await async_transfer_playback(self.mocks["hass"], self.mocks["call"])

    def test_call_data_updated(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": None,
                "data": {}
            }

        )

    def test_play_media_was_called(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()


class TestTransferOfInactivePlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_rebuild_playback")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
            self,
            mock_play: AsyncMock,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
            mock_rebuild: AsyncMock,
    ):
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
            "account": mock_account.return_value,
            "entry": mock_entry.return_value,
            "rebuild": mock_rebuild,
        }

        self.mocks["account"].async_playback_state = AsyncMock(
            return_value={}
        )
        self.mocks["account"].async_last_playback_state = AsyncMock()
        self.mocks["account"].async_last_playback_state.return_value = {
            "device": "foo",
            "context": {"uri": "bar"},
        }

        self.mocks["rebuild"].return_value = {"context": "modified"}

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }

        await async_transfer_playback(self.mocks["hass"], self.mocks["call"])

    def test_call_data_properly_modified(self):
        self.assertEqual(self.mocks["call"].data, {"context": "modified"})

    def test_async_play_media_called(self):
        try:
            self.mocks["play"].assert_called()
        except AssertionError:
            self.fail()


class TestTransferOfMissingPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_rebuild_playback")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
            self,
            mock_play: AsyncMock,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
            mock_rebuild: AsyncMock,
    ):
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
            "account": mock_account.return_value,
            "entry": mock_entry.return_value,
            "rebuild": mock_rebuild,
        }

        self.mocks["account"].async_playback_state = AsyncMock(
            return_value={}
        )
        self.mocks["account"].async_last_playback_state = AsyncMock()
        self.mocks["account"].async_last_playback_state.return_value = {}

        self.mocks["rebuild"].return_value = {"context": "modified"}
        self.mocks["account"].liked_songs_uri = "spotify:user:foo:collection"

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }

        await async_transfer_playback(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_play_media_called_with_liked_songs_uri(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:user:foo:collection",
                "data": {}
            },
        )
