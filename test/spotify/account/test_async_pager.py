"""Module to test the async_pager function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
    Spotify
)

TEST_MODULE = "custom_components.spotcast.spotify.account"


class TestPagingApiEndpoint(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.side_effect = [
            {
                "total": 3,
                "offset": 0,
                "items": ["foo", "bar"]
            },
            {
                "total": 3,
                "offset": 2,
                "items": ["baz"]
            },
        ]

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            internal_session=self.mocks["internal"],
            external_session=self.mocks["external"],
        )
        self.account._spotify.dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account._spotify.dummy_endpoint
        )

    def test_proper_result_retrieved(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_endpoint_called_2_times(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            2,
        )


class TestPagingWithLimit(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.side_effect = [
            {
                "total": 5,
                "offset": 0,
                "items": ["foo", "bar"]
            },
            {
                "total": 5,
                "offset": 2,
                "items": ["baz", "boo"]
            },
            {
                "total": 5,
                "offset": 2,
                "items": ["far"]

            },
        ]

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            internal_session=self.mocks["internal"],
            external_session=self.mocks["external"],
        )
        self.account._spotify.dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account._spotify.dummy_endpoint,
            max_items=3,
        )

    def test_proper_result_retrieved(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_endpoint_called_2_times(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            2,
        )


class TestSubLayeredPager(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.side_effect = [
            {
                "foo": {
                    "total": 3,
                    "offset": 0,
                    "items": ["foo", "bar"]
                }
            },
            {
                "foo": {
                    "total": 3,
                    "offset": 2,
                    "items": ["baz"]
                }
            },
        ]

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            internal_session=self.mocks["internal"],
            external_session=self.mocks["external"],
        )
        self.account._spotify.dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account._spotify.dummy_endpoint,
            sub_layer="foo"
        )

    def test_proper_result_retrieved(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_endpoint_called_2_times(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            2,
        )
