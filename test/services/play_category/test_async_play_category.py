"""Module to test the async_play_category function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.play_category import (
    async_play_category,
    SpotifyAccount,
    HomeAssistant,
    ServiceCall,
)
from custom_components.spotcast.services.exceptions import InvalidCategoryError

TEST_MODULE = "custom_components.spotcast.services.play_category"


class TestCategoryName(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.choice", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_choice: MagicMock,
            mock_play: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)
        mock_choice.return_value = {"uri": "bar", "name": "bar playlist"}

        self.mocks = {
            "account": mock_account.return_value,
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
        }

        self.mocks["account"].async_categories.return_value = [
            {"id": "12345", "name": "dummy"},
            {"id": "23456", "name": "foo"},
            {"id": "34567", "name": "category"},
        ]

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "category": "category"
        }

        self.mocks["account"].async_category_playlists.return_value = [
            {"uri": "foo", "name": "foo playlist"},
            {"uri": "bar", "name": "bar playlist"},
            {"uri": "baz", "name": "baz playlist"},
        ]

        await async_play_category(self.mocks["hass"], self.mocks["call"])

    def test_async_play_media_called_with_proper_arguments(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_was_properly_modified(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "bar"
            }
        )

    def test_playlist_retrieved_from_expected_category(self):
        try:
            self.mocks["account"].async_category_playlists.assert_called_with(
                "34567"
            )
        except AssertionError:
            self.fail()


class TestCategoryId(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.choice", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_choice: MagicMock,
            mock_play: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)
        mock_choice.return_value = {"uri": "bar", "name": "bar playlist"}

        self.mocks = {
            "account": mock_account.return_value,
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
        }

        self.mocks["account"].async_categories.return_value = [
            {"id": "12345", "name": "dummy"},
            {"id": "23456", "name": "foo"},
            {"id": "34567", "name": "category"},
        ]

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "category": "23456"
        }

        self.mocks["account"].async_category_playlists.return_value = [
            {"uri": "foo", "name": "foo playlist"},
            {"uri": "bar", "name": "bar playlist"},
            {"uri": "baz", "name": "baz playlist"},
        ]

        await async_play_category(self.mocks["hass"], self.mocks["call"])

    def test_async_play_media_called_with_proper_arguments(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_was_properly_modified(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "bar"
            }
        )

    def test_playlist_retrieved_from_expected_category(self):
        try:
            self.mocks["account"].async_category_playlists.assert_called_with(
                "23456"
            )
        except AssertionError:
            self.fail()


class TestCategoryNotFound(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.choice", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_error_raises(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_choice: MagicMock,
            mock_play: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)
        mock_choice.return_value = {"uri": "bar", "name": "bar playlist"}

        self.mocks = {
            "account": mock_account.return_value,
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
        }

        self.mocks["account"].async_categories.return_value = [
            {"id": "12345", "name": "dummy"},
            {"id": "23456", "name": "foo"},
            {"id": "34567", "name": "category"},
        ]

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "category": "98765"
        }

        self.mocks["account"].async_category_playlists.return_value = [
            {"uri": "foo", "name": "foo playlist"},
            {"uri": "bar", "name": "bar playlist"},
            {"uri": "baz", "name": "baz playlist"},
        ]

        with self.assertRaises(InvalidCategoryError):
            await async_play_category(self.mocks["hass"], self.mocks["call"])


class TestLimitCategorySize(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    @patch(f"{TEST_MODULE}.choice", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_choice: MagicMock,
            mock_play: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_entry.return_value = MagicMock(spec=ConfigEntry)
        mock_choice.return_value = {"uri": "bar", "name": "bar playlist"}

        self.mocks = {
            "account": mock_account.return_value,
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play": mock_play,
            "choice": mock_choice,
        }

        self.mocks["account"].async_categories.return_value = [
            {"id": "12345", "name": "dummy"},
            {"id": "23456", "name": "foo"},
            {"id": "34567", "name": "category"},
        ]

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "category": "23456",
            "data": {
                "limit": 2
            }
        }

        self.playlists = [
            {"uri": "foo", "name": "foo playlist"},
            {"uri": "bar", "name": "bar playlist"},
            {"uri": "baz", "name": "baz playlist"},
        ]

        self.mocks["account"].async_category_playlists\
            .return_value = self.playlists
        await async_play_category(self.mocks["hass"], self.mocks["call"])

    def test_async_play_media_called_with_proper_arguments(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_was_properly_modified(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "bar",
                "data": {
                    "limit": 2
                }
            }
        )

    def test_playlist_retrieved_from_expected_category(self):
        try:
            self.mocks["account"].async_category_playlists.assert_called_with(
                "23456"
            )
        except AssertionError:
            self.fail()

    def test_choice_was_called_with_subset_of_playlist(self):
        try:
            self.mocks["choice"].assert_called_with(
                self.playlists[:2]
            )
        except AssertionError:
            self.fail()
