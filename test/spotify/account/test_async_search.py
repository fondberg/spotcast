"""Module to test the async_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
    SearchQuery,
)


class TestSearchQuery(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "_async_pager")
    async def asyncSetUp(self, mock_pager: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "pager": mock_pager,
        }

        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
        )
        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.query = SearchQuery(
            search="foo",
            item_type="artist",
        )

        self.result = await self.account.async_search(self.query)

    def test_proper_result_provided(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])


class TestHighMaxItems(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "_async_pager")
    async def asyncSetUp(self, mock_pager: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "pager": mock_pager,
        }

        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
        )
        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.query = SearchQuery(
            search="foo",
            item_type="artist",
        )

        self.result = await self.account.async_search(self.query, max_items=60)

    def test_proper_result_provided(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])
