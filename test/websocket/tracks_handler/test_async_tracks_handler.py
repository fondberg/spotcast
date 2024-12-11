"""Module to test the async_tracks_handler function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.tracks_handler import (
    async_tracks_handler,
    HomeAssistant,
    ActiveConnection,
)

from test.websocket.tracks_handler import TEST_MODULE


class TestBasicRequest(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_account")
    async def asyncSetUp(self, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "connection": MagicMock(spec=ActiveConnection),
            "account": mock_account.return_value,
        }

        self.mocks["account"].id = "12345"
        self.mocks["account"].async_get_playlist_tracks = AsyncMock(
            return_value=[
                {
                    "track": {
                        "id": "foo",
                        "name": "Foo",
                        "uri": "spotify:track:foo",
                        "album": {"uri": "spotify:album:foo"},
                        "artists": [
                            {"uri": "spotify:artist:foo"}
                        ]
                    }
                },
                {
                    "track": {
                        "id": "bar",
                        "name": "Bar",
                        "uri": "spotify:track:bar",
                        "album": {"uri": "spotify:album:bar"},
                        "artists": [
                            {"uri": "spotify:artist:bar"}
                        ]
                    }
                },
                {
                    "track": {
                        "id": "baz",
                        "name": "Baz",
                        "uri": "spotify:track:baz",
                        "album": {"uri": "spotify:album:baz"},
                        "artists": [
                            {"uri": "spotify:artist:baz"}
                        ]
                    }
                },
            ],
        )

        await async_tracks_handler(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1, "playlist_id": "spotify:playlist:foo"}
        )

    def test_result_properly_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 3,
                    "account": "12345",
                    "tracks": [
                        {
                            "id": "foo",
                            "name": "Foo",
                            "uri": "spotify:track:foo",
                            "album": {"uri": "spotify:album:foo"},
                            "artists": [
                                {"uri": "spotify:artist:foo"}
                            ]
                        },
                        {
                            "id": "bar",
                            "name": "Bar",
                            "uri": "spotify:track:bar",
                            "album": {"uri": "spotify:album:bar"},
                            "artists": [
                                {"uri": "spotify:artist:bar"}
                            ]
                        },
                        {
                            "id": "baz",
                            "name": "Baz",
                            "uri": "spotify:track:baz",
                            "album": {"uri": "spotify:album:baz"},
                            "artists": [
                                {"uri": "spotify:artist:baz"}
                            ]
                        },
                    ]
                }
            )
        except AssertionError:
            self.fail()
