"""Module to test the async_saved_episodes function"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PrivateSession,
    HomeAssistant,
    PublicSession,
    Spotify,
)

from test.spotify.account import TEST_MODULE


class TestDatasetFresh(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_spotify: MagicMock,
    ):

        mock_spotify.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "internal": MagicMock(spec=PrivateSession),
            "external": MagicMock(spec=PublicSession),
            "hass": MagicMock(spec=HomeAssistant),
            "spotify": mock_spotify.return_value,
        }
        self.mocks["hass"].loop = MagicMock()
        self.mocks["spotify"].current_user_saved_episodes = MagicMock()
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
        self.account._datasets["profile"]._data = {
            "name": "Dummy",
            "country": "CA"
        }

        self.account._async_pager = AsyncMock(return_value=[
            "foo",
            "bar",
            "baz"
        ])

        self.result = await self.account.async_saved_episodes()

    def test_pager_properly_called(self):
        try:
            self.account._async_pager.assert_called_with(
                self.account.apis["private"].current_user_saved_episodes,
                appends=["CA"],
                max_items=None
            )
        except AssertionError:
            self.fail()

    def test_recieved_expected_data(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])
