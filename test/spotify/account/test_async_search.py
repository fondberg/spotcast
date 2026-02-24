"""Module to test the async_search function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    SearchQuery,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestSearchQuery(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "_async_pager")
    async def asyncSetUp(self, mock_pager: AsyncMock, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "pager": mock_pager,
        }

        self.mocks["pager"].return_value = ["foo", "bar", "baz"]

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )
        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.query = SearchQuery(
            search="foo",
            item_types="artist",
        )

        self.mocks["hass"].async_add_executor_job = AsyncMock(
            return_value={"artists": {"items": ["foo", "bar", "baz"]}}
        )

        self.result = await self.account.async_search(self.query)

    def test_proper_result_provided(self):
        self.assertEqual(self.result, {"artists": ["foo", "bar", "baz"]})


class TestSearchQueryNullItems(IsolatedAsyncioTestCase):
    """Tests that async_search handles None and null items from the Spotify API."""

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch.object(SpotifyAccount, "_async_pager")
    async def asyncSetUp(self, mock_pager: AsyncMock, mock_store: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
        )
        self.account._datasets["profile"].expires_at = time() + 999
        self.account._datasets["profile"]._data = {"country": "CA"}

        self.query = SearchQuery(
            search="foo",
            item_types="artist",
        )

    async def _run_search(self, api_return_value: dict) -> dict:
        self.mocks["hass"].async_add_executor_job = AsyncMock(
            return_value=api_return_value
        )
        return await self.account.async_search(self.query)

    async def test_null_items_list_returns_empty(self):
        """Spotify API sometimes returns None for items when a category has no results."""
        result = await self._run_search({"artists": {"items": None}})
        self.assertEqual(result, {"artists": []})

    async def test_items_containing_none_values_are_filtered(self):
        """Spotify API sometimes returns [None] in items for certain result types."""
        result = await self._run_search({"artists": {"items": [None, "foo", None, "bar"]}})
        self.assertEqual(result, {"artists": ["foo", "bar"]})
