"""Module to test the async_last_playback_state function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestExistingState(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    async def asyncSetUp(self, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": MagicMock(spec=PrivateSession),
            "public": MagicMock(spec=PublicSession),
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
            is_default=True,
            base_refresh_rate=30,
        )
        self.account._last_playback_state = {"foo": "bar"}

        self.result = await self.account.async_last_playback_state()

    def test_known_last_playback_state(self):
        self.assertEqual(self.result, {"foo": "bar"})


class TestNoState(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    async def asyncSetUp(self, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": MagicMock(spec=PrivateSession),
            "public": MagicMock(spec=PublicSession),
            "store": mock_store.return_value,
        }

        self.mocks["store"].async_load = AsyncMock()
        self.mocks["store"].async_load.return_value = {"foo": "bar"}

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
            is_default=True,
            base_refresh_rate=30,
        )
        self.account._last_playback_state = {}

        self.result = await self.account.async_last_playback_state()

    def test_known_last_playback_state(self):
        self.assertEqual(self.result, {"foo": "bar"})
