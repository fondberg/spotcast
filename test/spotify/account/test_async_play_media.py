"""Module to test the async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    PlaybackError,
    SpotifyException,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestMediaPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
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
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        await self.account.async_play_media(
            "foo",
            "spotify:dummy:uri"
        )

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].start_playback,
                "foo",
                "spotify:dummy:uri",
                None,
                None,
                None,
            )
        except AssertionError:
            self.fail()


class TestEmptyContext(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
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
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        await self.account.async_play_media("foo")

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].transfer_playback,
                "foo",
                True
            )
        except AssertionError:
            self.fail()


class TestFailedTransfer(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
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
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock(
            side_effect=SpotifyException(403, "foo", "bar")
        )

        with self.assertRaises(PlaybackError):
            await self.account.async_play_media("foo")

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].transfer_playback,
                "foo",
                True
            )
        except AssertionError:
            self.fail()


class TestMediaPlaybackWithExtras(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
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
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        await self.account.async_play_media(
            "foo",
            "spotify:dummy:uri",
            offset=2,
            position=2.5346,
        )

    def test_play_media_was_called(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].start_playback,
                "foo",
                "spotify:dummy:uri",
                None,
                {"position": 2},
                2534,
            )
        except AssertionError:
            self.fail()


class TestPlaybackError(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def test_error_raised(
            self,
            mock_spotify: MagicMock,
            mock_store: MagicMock,
    ):

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
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
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.async_ensure_tokens_valid = AsyncMock()

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {"name": "Dummy"}

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job\
            .side_effect = SpotifyException(MagicMock(), 418, "I'm a teapot'")

        with self.assertRaises(PlaybackError):
            await self.account.async_play_media(
                "foo",
                "spotify:dummy:uri"
            )
