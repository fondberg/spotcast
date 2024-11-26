"""Module to test the async_ensure_tokens_valid function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    TokenError,
    ConfigEntry,
    SOURCE_REAUTH,
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
            entry_id="12345",
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
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
            self.account._spotify.set_auth.assert_any_call(
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

        self.mocks["internal"].token = "23456"

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
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
            self.account._spotify.set_auth.assert_any_call(
                "12345"
            )
        except AssertionError:
            self.fail()

    def test_internal_controller_token_updated_after_refresh(self):
        try:
            self.account._spotify.set_auth.assert_any_call("23456")
        except AssertionError:
            self.fail()


class TestTokenErrorHandling(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify")
    async def test_reauth_process_not_called_when_not_requested(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
        }
        self.mocks["hass"].loop = MagicMock()
        self.mocks["hass"].config_entries.async_get_entry\
            .return_value = self.mocks["entry"]

        self.mock_spotify = mock_spotify

        self.mocks["internal"].async_ensure_token_valid = AsyncMock()
        self.mocks["internal"].async_ensure_token_valid\
            .side_effect = TokenError()

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_profile = AsyncMock()

        with self.assertRaises(TokenError):
            await self.account.async_ensure_tokens_valid(reauth_on_fail=False)

        try:
            self.mocks["entry"].async_start_reauth.assert_not_called()
        except AssertionError:
            self.fail()

    @patch(f"{TEST_MODULE}.Spotify")
    async def test_reauth_process_called_when_requested(
            self,
            mock_spotify: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=InternalSession),
            "external": MagicMock(spec=OAuth2Session),
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry),
        }
        self.mocks["hass"].loop = MagicMock()
        self.mocks["hass"].config_entries.async_get_entry\
            .return_value = self.mocks["entry"]

        self.mock_spotify = mock_spotify

        self.mocks["internal"].async_ensure_token_valid = AsyncMock()
        self.mocks["internal"].async_ensure_token_valid\
            .side_effect = TokenError()

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_profile = AsyncMock()

        with self.assertRaises(TokenError):
            await self.account.async_ensure_tokens_valid()

        try:
            self.mocks["entry"].async_start_reauth.assert_called_with(
                self.mocks["hass"],
                context={"source": SOURCE_REAUTH},
            )
        except AssertionError:
            self.fail()
