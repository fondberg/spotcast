"""Module to test the async_apply_extras function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession
)


class TestExtraApplied(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_repeat")
    @patch.object(SpotifyAccount, "async_shuffle")
    @patch.object(SpotifyAccount, "async_set_volume")
    async def asyncSetUp(
        self,
        mock_volume: AsyncMock,
        mock_shuffle: AsyncMock,
        mock_repeat: AsyncMock,
    ):

        self.mocks: dict[str, MagicMock] = {}
        self.mocks["volume"] = mock_volume
        self.mocks["shuffle"] = mock_shuffle
        self.mocks["repeat"] = mock_repeat
        self.mocks["hass"] = MagicMock(spec=HomeAssistant)

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        self.account = SpotifyAccount(
            self.mocks["hass"],
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        await self.account.async_apply_extras(
            "12345",
            {
                "start_volume": 80,
                "shuffle": True,
                "repeat": "context",
                "position": 4,
            }
        )

    async def test_async_repeat_called(self):
        try:
            self.mocks["repeat"].assert_called_with("context", "12345")
        except AssertionError:
            self.fail()

    async def test_async_shuffle_called(self):
        try:
            self.mocks["shuffle"].assert_called_with(True, "12345")
        except AssertionError:
            self.fail()

    async def test_async_set_volume_called(self):
        try:
            self.mocks["volume"].assert_called_with(80, "12345")
        except AssertionError:
            self.fail()
