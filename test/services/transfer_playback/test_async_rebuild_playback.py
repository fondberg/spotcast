"""Module to test async_rebuild_playback"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.transfer_playback import (
    async_rebuild_playback,
    SpotifyAccount,
)

from test.services.transfer_playback import TEST_MODULE


class TestRepeatOveride(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:album:foo",
                "type": "album"
            },
        }

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "offset": 2,
                "position": 5
            }
        }

    async def test_repeat_is_not_set(self):
        self.call_data["data"]["repeat"] = "off"
        result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

        self.assertEqual(result["data"]["repeat"], "off")

    async def test_repeat_was_set(self):
        result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

        self.assertEqual(result["data"]["repeat"], "context")


class TestShuffleOveride(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:album:foo",
                "type": "album"
            },
        }

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "offset": 2,
                "position": 5,
            }
        }

    async def test_repeat_is_not_set(self):
        self.call_data["data"]["shuffle"] = False
        result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

        self.assertFalse(result["data"]["shuffle"])

    async def test_repeat_was_set(self):
        result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

        self.assertTrue(result["data"]["shuffle"])


class TestCurrentItemIsPartOfAlbumContext(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:album:foo",
                "type": "album"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:foo"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["index"].return_value = 4

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:album:foo",
                "data": {
                    "offset": 4,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )


class TestCurrentItemNotPartOfAlbumContext(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:album:foo",
                "type": "album"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["index"].side_effect = ValueError()

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:album:foo",
                "data": {
                    "offset": 0,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )


class TestCurrentItemPartOfPlaylist(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:playlist:foo",
                "type": "playlist"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["account"].async_get_playlist_tracks = AsyncMock(
            return_value=[
                {"uri": "spotify:track:foo"},
                {"uri": "spotify:track:bar"},
                {"uri": "spotify:track:baz"},
            ]
        )

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:playlist:foo",
                "data": {
                    "offset": 1,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )

    def test_track_index_not_called(self):
        try:
            self.mocks["index"].assert_not_called()
        except AssertionError:
            self.fail()


class TestCurrentItemNotPartOfPlaylist(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:playlist:foo",
                "type": "playlist"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["account"].async_get_playlist_tracks = AsyncMock(
            return_value=[
                {"uri": "spotify:track:foo"},
                {"uri": "spotify:track:far"},
                {"uri": "spotify:track:baz"},
            ]
        )

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:playlist:foo",
                "data": {
                    "offset": 0,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )

    def test_track_index_not_called(self):
        try:
            self.mocks["index"].assert_not_called()
        except AssertionError:
            self.fail()


class TestCurrentItemPartOfCollection(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "progress_ms": 31415,
            "context": {
                "uri": "spotify:user:dummy:collection",
                "type": "collection"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["account"].async_liked_songs = AsyncMock(
            return_value=[
                "spotify:track:foo",
                "spotify:track:bar",
                "spotify:track:baz",
            ]
        )

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {}
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:user:dummy:collection",
                "data": {
                    "offset": 1,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 31.415
                }
            }
        )

    def test_track_index_not_called(self):
        try:
            self.mocks["index"].assert_not_called()
        except AssertionError:
            self.fail()


class TestCurrentItemNotPartOfCollection(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:user:dummy:collection",
                "type": "collection"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["account"].async_liked_songs = AsyncMock(
            return_value=[
                {"uri": "spotify:track:foo"},
                {"uri": "spotify:track:far"},
                {"uri": "spotify:track:baz"},
            ]
        )

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:user:dummy:collection",
                "data": {
                    "offset": 0,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )

    def test_track_index_not_called(self):
        try:
            self.mocks["index"].assert_not_called()
        except AssertionError:
            self.fail()


class TestUnknownContentType(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    async def asyncSetUp(self, mock_index: AsyncMock):

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "index": mock_index,
        }

        self.mocks["account"].last_playback_state = {
            "repeat_state": "context",
            "shuffle_state": True,
            "context": {
                "uri": "spotify:user:dummy:collection",
                "type": "dummy"
            },
            "item": {
                "album": {
                    "uri": "spotify:album:baz"
                },
                "uri": "spotify:track:bar"
            }
        }

        self.mocks["account"].async_liked_songs = AsyncMock(
            return_value=[
                {"uri": "spotify:track:foo"},
                {"uri": "spotify:track:far"},
                {"uri": "spotify:track:baz"},
            ]
        )

        self.call_data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "position": 5
            }
        }

        self.result = await async_rebuild_playback(
            self.call_data,
            self.mocks["account"],
        )

    def test_returned_expected_call_data(self):
        self.assertEqual(
            self.result,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "spotify_uri": "spotify:user:dummy:collection",
                "data": {
                    "offset": 0,
                    "shuffle": True,
                    "repeat": "context",
                    "position": 5
                }
            }
        )

    def test_track_index_not_called(self):
        try:
            self.mocks["index"].assert_not_called()
        except AssertionError:
            self.fail()
