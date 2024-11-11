"""Module to test async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from custom_components.spotcast.services.play_media import (
    async_play_media,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_media"


class TestBaseMediaPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id", new_callable=AsyncMock)
    @patch.object(SpotifyAccount, "async_from_config_entry", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.get_account_entry")
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: MagicMock,
        mock_player: MagicMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "volume": 80
            }
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].async_play_media\
                .assert_called_with("12345", "dummy_uri", volume=80)
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()


class TestEmptyExtras(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id", new_callable=AsyncMock)
    @patch.object(SpotifyAccount, "async_from_config_entry", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.get_account_entry")
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: MagicMock,
        mock_player: MagicMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].return_value.async_play_media\
                .assert_called_with("12345", "dummy_uri")
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].return_value.async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()
