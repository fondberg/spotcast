"""Module to test the async_episode_index function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from custom_components.spotcast.services.play_media import (
    async_episode_index,
    SpotifyAccount,
)


class TestEpisodeIndexRetrieval(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.mocks["account"].async_get_episode = AsyncMock(return_value={
            "show": {
                "uri": "spotify:show:bar"
            }
        })

        self.mocks["account"].async_get_show_episodes = AsyncMock(return_value=[
            {"uri": "spotify:episode:bar"},
            {"uri": "spotify:episode:foo"},
            {"uri": "spotify:episode:baz"},
        ])

        self.result = await async_episode_index(
            account=self.mocks["account"],
            uri="spotify:episode:foo",
        )

    def test_reply_has_proper_format(self):
        self.assertIsInstance(self.result, tuple)
        self.assertEqual(len(self.result), 2)
        self.assertIsInstance(self.result[0], str)
        self.assertIsInstance(self.result[1], int)

    def test_proper_show_rui_returned(self):
        self.assertEqual(self.result[0], "spotify:show:bar")

    def test_proper_index_returned(self):
        self.assertEqual(self.result[1], 1)
