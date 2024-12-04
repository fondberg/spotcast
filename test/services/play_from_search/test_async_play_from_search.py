"""Module to test the async_play_from_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_from_search import (
    async_play_from_search,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_from_search"


class TestTrackSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.async_play_custom_context")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
            mock_play_media: AsyncMock,
            mock_play_search: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock()

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry.return_value,
            "account": mock_account.return_value,
            "play_media": mock_play_media,
            "play_search": mock_play_search,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "search_term": "foo",
            "item_type": "track",
            "tags": ["new"],
            "filters": {
                "artist": "bar"
            }
        }

        self.mocks["account"].async_search = AsyncMock()
        self.mocks["account"].async_search.return_value = [
            {"uri": "foo"},
            {"uri": "bar"},
            {"uri": "baz"},
        ]

        await async_play_from_search(self.mocks["hass"], self.mocks["call"])

    def test_proper_service_call_made(self):
        try:
            self.mocks["play_media"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()


class TestAlbumSearch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.async_play_custom_context")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
            mock_play_media: AsyncMock,
            mock_play_search: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock()

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry.return_value,
            "account": mock_account.return_value,
            "play_media": mock_play_media,
            "play_search": mock_play_search,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "search_term": "foo",
            "item_type": "album",
            "filters": {
                "artist": "bar"
            }
        }

        self.mocks["account"].async_search = AsyncMock()
        self.mocks["account"].async_search.return_value = [
            {"uri": "foo"},
        ]

        await async_play_from_search(self.mocks["hass"], self.mocks["call"])

    def test_proper_service_call_made(self):
        try:
            self.mocks["play_search"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()


class TestModifiedLimit(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.async_play_custom_context")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry")
    async def asyncSetUp(
            self,
            mock_entry: AsyncMock,
            mock_account: AsyncMock,
            mock_play_media: AsyncMock,
            mock_play_search: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock()

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry.return_value,
            "account": mock_account.return_value,
            "play_media": mock_play_media,
            "play_search": mock_play_search,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "search_term": "foo",
            "item_type": "track",
            "filters": {
                "artist": "bar"
            },
            "data": {
                "limit": 2
            }
        }

        self.mocks["account"].async_search = AsyncMock()
        self.mocks["account"].async_search.return_value = [
            {"uri": "foo"},
            {"uri": "bar"},
        ]

        await async_play_from_search(self.mocks["hass"], self.mocks["call"])

    def test_proper_service_call_made(self):
        try:
            self.mocks["play_media"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()
