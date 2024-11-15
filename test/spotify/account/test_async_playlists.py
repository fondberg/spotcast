"""Module to test the async_playlists function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestDatasetFresh(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}
        self.account._datasets["playlists"].expires_at = time() + 9999
        self.account._datasets["playlists"]._data = [
            "foo",
            "bar"
        ]

        self.result = await self.account.async_playlists()

    def test_new_profile_was_not_fetched(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_not_called()
        except AssertionError:
            self.fail()

    def test_profile_retrieved_was_expected(self):
        self.assertEqual(self.result, ["foo", "bar"])


class TestDatasetExpired(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "_async_pager")
    @patch(f"{TEST_MODULE}.Spotify")
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_pager: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
            "pager": mock_pager
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}
        self.account._datasets["playlists"].expires_at = time() - 9999
        self.account._datasets["playlists"]._data = {"foo": "bar"}
        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.result = await self.account.async_playlists()

    def test_new_profile_was_fetched(self):
        try:
            self.mocks["pager"].assert_called_with(
                self.account._spotify.current_user_playlists,
                max_items=None
            )
        except AssertionError:
            self.fail()

    def test_profile_retrieved_was_expected(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])


class TestForceRefresh(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "_async_pager")
    @patch(f"{TEST_MODULE}.Spotify")
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_pager: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
            "pager": mock_pager,
        }
        self.mocks["hass"].loop = MagicMock()

        self.mock_spotify = mock_spotify

        self.mocks["external"].token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            self.mocks["hass"],
            self.mocks["external"],
            self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}
        self.account._datasets["playlists"].expires_at = time() + 9999
        self.account._datasets["playlists"]._data = {"foo": "bar"}
        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.result = await self.account.async_playlists(force=True)

    def test_new_profile_was_fetched(self):
        try:
            self.mocks["pager"].assert_called_with(
                self.account._spotify.current_user_playlists,
                max_items=None,
            )
        except AssertionError:
            self.fail()

    def test_profile_retrieved_was_expected(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])
