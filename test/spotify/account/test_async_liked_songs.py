"""Module to test the async_liked_songs function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestMediaCasting(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant, new_callable=AsyncMock)

        self.mock_hass.async_add_executor_job = AsyncMock()
        self.mock_hass.async_add_executor_job.side_effect = [
            {
                "limit": 2,
                "offset": 0,
                "total": 3,
                "items": [
                    {"track": {"uri": "foo"}},
                    {"track": {"uri": "bar"}},
                ]
            },
            {
                "limit": 2,
                "offset": 2,
                "total": 3,
                "items": [
                    {"track": {"uri": "baz"}},
                ]
            }
        ]

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.account._profile = {
            "name": "dummy user"
        }

        self.result = await self.account.async_liked_songs()

    def test_received_expected_ammount_of_uris(self):
        self.assertEqual(len(self.result), 3)
