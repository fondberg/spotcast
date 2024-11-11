"""Module to test the clean_playlist function"""

from unittest import TestCase

from custom_components.spotcast.sensor.spotify_playlists_sensor import (
    SpotifyPlaylistsSensor
)


class TestStandardPlaylist(TestCase):

    def setUp(self):
        self.playlist = {
            "collaborative": False,
            "description": "Playlist Description",
            "external_urls": {
                "spotify": "https://open.spotify.com/playlist/12345"
            },
            "href": "https://api.spotify.com/v1/playlists/12345",
            "id": "12345",
            "images": [
                {
                    "url": "https://mosaic.scdn.co/640/foo",
                    "height": 640,
                    "width": 640
                },
                {
                    "url": "https://mosaic.scdn.co/300/foo",
                    "height": 300,
                    "width": 300
                },
                {
                    "url": "https://mosaic.scdn.co/0/foo",
                    "height": None,
                    "width": None,
                }
            ],
            "name": "Dummy Playlist",
            "owner": {
                "external_urls": {
                    "spotify": "https://open.spotify.com/user/dummy_id"
                },
                "href": "https://api.spotify.com/v1/users/dummy_id",
                "id": "dummy_id",
                "type": "user",
                "uri": "spotify:user:dummy_id",
                "display_name": "Dummy Account"
            },
            "public": True,
            "snapshot_id": "AAAAevyVpJ+p+NxtC6pr1bECoDk30g0p",
            "tracks": {
                "href": "https://api.spotify.com/v1/playlists/12345/tracks",
                "total": 121
            },
            "type": "playlist",
            "uri": "spotify:playlist:12345",
            "primary_color": None
        }

        self.result = SpotifyPlaylistsSensor._clean_playlist(self.playlist)

    def test_expected_playlist_value_returned(self):
        self.assertEqual(
            self.result,
            {
                "collaborative": False,
                "description": "Playlist Description",
                "image": "https://mosaic.scdn.co/640/foo",
                "name": "Dummy Playlist",
                "owner": "dummy_id",
                "uri": "spotify:playlist:12345",
            }
        )
