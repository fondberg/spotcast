"""Module to test the async_ensure_tokens_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestWithProfileRefresh(IsolatedAsyncioTestCase):

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

        self.account.async_profile = AsyncMock()

        await self.account.async_ensure_tokens_valid()

    def test_async_profile_was_called(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_both_sessions_were_checked_for_token(self):
        for key, session in self.account.sessions.items():
            try:
                session.async_ensure_token_valid.assert_called()
            except AssertionError:
                self.fail()

    def test_spotify_token_updated_after_refresh(self):
        try:
            self.account._spotify.set_auth.assert_called_with(
                "12345"
            )
        except AssertionError:
            self.fail()


class TestWithoutProfileRefresh(IsolatedAsyncioTestCase):

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

        self.account.async_profile = AsyncMock()

        await self.account.async_ensure_tokens_valid(skip_profile=True)

    def test_async_profile_was_not_called(self):
        try:
            self.account.async_profile.assert_not_called()
        except AssertionError:
            self.fail()

    def test_both_sessions_were_checked_for_token(self):
        for key, session in self.account.sessions.items():
            try:
                session.async_ensure_token_valid.assert_called()
            except AssertionError:
                self.fail()

    def test_spotify_token_updated_after_refresh(self):
        try:
            self.account._spotify.set_auth.assert_called_with(
                "12345"
            )
        except AssertionError:
            self.fail()
