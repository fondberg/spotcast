"""Module to test the async_get_playlist function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PrivateSession,
    PublicSession,
    HomeAssistant,
    Spotify,
)

from test.spotify.account import TEST_MODULE

API_RESULT = {
    "collaborative": False,
    "description": ...,
    "external_urls": {
        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX58NJL8iVBGW"
    },
    "followers": {
        "href": None,
        "total": 783040
    },
    "href": ...,
    "id": "37i9dQZF1DX58NJL8iVBGW",
    "images": [
        {
            "url": ...,
            "height": None,
            "width": None
        }
    ],
    "name": "Southern Gothic",
    "owner": {
        "external_urls": {
            "spotify": "https://open.spotify.com/user/spotify"
        },
        "href": "https://api.spotify.com/v1/users/spotify",
        "id": "spotify",
        "type": "user",
        "uri": "spotify:user:spotify",
        "display_name": "Spotify"
    },
    "public": True,
    "snapshot_id": "ZohAYAAAAACymN7Vf+uqFL33SFnd8EaM",
    "tracks": {
        "href": ...,
        "limit": 100,
        "next": None,
        "offset": 0,
        "previous": None,
        "total": 100,
        "items": [...]
    }
}


class TestPlayslistRetrieval(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=PublicSession),
            "internal": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify,
        }

        self.mocks["hass"].async_add_executor_job = AsyncMock()
        self.mocks["hass"].async_add_executor_job.return_value = API_RESULT

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            private_session=self.mocks["internal"],
            public_session=self.mocks["external"],
        )

        self.account._datasets["profile"].expires_at = time() + 9999
        self.account._datasets["profile"]._data = {
            "country": "CA"
        }

        self.result = await self.account.async_get_playlist(
            "spotify:playlist:foo"
        )

    def test_proper_result_returned(self):
        self.assertEqual(API_RESULT, self.result)

    def test_proper_call_to__executor(self):
        try:
            self.mocks["hass"].async_add_executor_job.assert_called_with(
                self.account.apis["private"].playlist,
                "foo",
                None,
                "CA",
            )
        except AssertionError:
            self.fail()
