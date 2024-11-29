"""Module to test the async_pager function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PublicSession,
    PrivateSession,
    HomeAssistant,
    Spotify
)

from test.spotify.account import TEST_MODULE


class TestPagingApiEndpoint(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
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
            entry_id="12345",
            hass=self.mocks["hass"],
            private_session=self.mocks["internal"],
            public_session=self.mocks["external"],
        )
        self.account.apis["private"].dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account.apis["private"].dummy_endpoint
        )

    def test_proper_result_retrieved(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_endpoint_called_2_times(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            2,
        )


class TestPagingWithLimit(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
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
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )
        self.account.apis["private"].dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account.apis["private"].dummy_endpoint,
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

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
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
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["external"],
            private_session=self.mocks["internal"],
            is_default=True
        )

        self.account.apis["private"].dummy_endpoint = MagicMock()

        self.result = await self.account._async_pager(
            self.account.apis["private"].dummy_endpoint,
            sub_layer="foo"
        )

    def test_proper_result_retrieved(self):
        self.assertEqual(self.result, ["foo", "bar", "baz"])

    def test_endpoint_called_2_times(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            2,
        )
