"""Module to test the liked songs property"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
from time import time

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    PublicSession,
    PrivateSession,
    Spotify,
    Store,
)

from test.spotify.account import TEST_MODULE


class TestLikedSongs(TestCase):

    @patch(f"{TEST_MODULE}.Store", spec=Store, new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    def setUp(self, mock_spotify: MagicMock, mock_store: MagicMock):

        mock_internal = MagicMock(spec=PrivateSession)
        mock_external = MagicMock(spec=PublicSession)

        self.mock_spotify = mock_spotify

        mock_external.token = {
            "access_token": "12345",
            "expires_at": 12345.61,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=MagicMock(spec=HomeAssistant),
            public_session=mock_external,
            private_session=mock_internal,
            is_default=True
        )

        self.liked_songs = [
            {
                "added_at": "2024-11-10T06:31:11Z",
                "track": {
                    "album": {
                            "album_type": "album",
                            "total_tracks": 13,
                            "available_markets": ["CA", "PR", "US"],
                            "external_urls": {
                                "spotify": "https://open.spotify.com/album/2qMIskI65m8Rr8dH5fNsUz"
                            },
                        "href": "https://api.spotify.com/v1/albums/2qMIskI65m8Rr8dH5fNsUz",
                        "id": "2qMIskI65m8Rr8dH5fNsUz",
                        "images": [
                                {
                                    "url": "https://i.scdn.co/image/ab67616d0000b2739dbbbaf7382943d74db1def1",
                                    "height": 640,
                                    "width": 640
                                },
                                {
                                    "url": "https://i.scdn.co/image/ab67616d00001e029dbbbaf7382943d74db1def1",
                                    "height": 300,
                                    "width": 300
                                },
                                {
                                    "url": "https://i.scdn.co/image/ab67616d000048519dbbbaf7382943d74db1def1",
                                    "height": 64,
                                    "width": 64
                                }
                                ],
                        "name": "We Need Medicine (Deluxe Edition)",
                        "release_date": "2013-10-07",
                        "release_date_precision": "day",
                        "type": "album",
                        "uri": "spotify:album:2qMIskI65m8Rr8dH5fNsUz",
                        "artists": [
                                {
                                    "external_urls": {
                                        "spotify": "https://open.spotify.com/artist/3M4ThdJR28z9eSMcQHAZ5G"
                                    },
                                    "href": "https://api.spotify.com/v1/artists/3M4ThdJR28z9eSMcQHAZ5G",
                                    "id": "3M4ThdJR28z9eSMcQHAZ5G",
                                    "name": "The Fratellis",
                                    "type": "artist",
                                    "uri": "spotify:artist:3M4ThdJR28z9eSMcQHAZ5G"
                                }
                                ],
                        "is_playable": True
                    },
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/3M4ThdJR28z9eSMcQHAZ5G"
                            },
                            "href": "https://api.spotify.com/v1/artists/3M4ThdJR28z9eSMcQHAZ5G",
                            "id": "3M4ThdJR28z9eSMcQHAZ5G",
                            "name": "The Fratellis",
                            "type": "artist",
                            "uri": "spotify:artist:3M4ThdJR28z9eSMcQHAZ5G"
                        }
                    ],
                    "available_markets": ["CA", "PR", "US"],
                    "disc_number": 1,
                    "duration_ms": 259840,
                    "explicit": False,
                    "external_ids": {
                        "isrc": "GB5KW1301067"
                    },
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/0FwjaMc01gWLe9sofzx27J"
                    },
                    "href": "https://api.spotify.com/v1/tracks/0FwjaMc01gWLe9sofzx27J",
                    "id": "0FwjaMc01gWLe9sofzx27J",
                    "is_playable": True,
                    "name": "Jeannie Nitro",
                    "popularity": 10,
                    "preview_url": "https://p.scdn.co/mp3-preview/9b959d2f6868d298cd04fd32b384f811c71caaf0?cid=cfe923b2d660439caf2b557b21f31221",
                    "track_number": 8,
                    "type": "track",
                    "uri": "spotify:track:0FwjaMc01gWLe9sofzx27J",
                    "is_local": False
                }
            },
            {
                "added_at": "2024-11-10T04:23:54Z",
                "track": {
                    "album": {
                            "album_type": "album",
                            "total_tracks": 10,
                            "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
                            "external_urls": {
                                "spotify": "https://open.spotify.com/album/0MQ3ILdZLlQOPWe9ypRcBl"
                            },
                        "href": "https://api.spotify.com/v1/albums/0MQ3ILdZLlQOPWe9ypRcBl",
                        "id": "0MQ3ILdZLlQOPWe9ypRcBl",
                        "images": [
                                {
                                    "url": "https://i.scdn.co/image/ab67616d0000b27321fb08c77e1a0586e115038b",
                                    "height": 640,
                                    "width": 640
                                },
                                {
                                    "url": "https://i.scdn.co/image/ab67616d00001e0221fb08c77e1a0586e115038b",
                                    "height": 300,
                                    "width": 300
                                },
                                {
                                    "url": "https://i.scdn.co/image/ab67616d0000485121fb08c77e1a0586e115038b",
                                    "height": 64,
                                    "width": 64
                                }
                                ],
                        "name": "Bastard Children (10th Anniversary)",
                        "release_date": "2022-12-30",
                        "release_date_precision": "day",
                        "type": "album",
                        "uri": "spotify:album:0MQ3ILdZLlQOPWe9ypRcBl",
                        "artists": [
                                {
                                    "external_urls": {
                                        "spotify": "https://open.spotify.com/artist/5Gu7iDoQjE7anHIbCXckC8"
                                    },
                                    "href": "https://api.spotify.com/v1/artists/5Gu7iDoQjE7anHIbCXckC8",
                                    "id": "5Gu7iDoQjE7anHIbCXckC8",
                                    "name": "Vudu Sister",
                                    "type": "artist",
                                    "uri": "spotify:artist:5Gu7iDoQjE7anHIbCXckC8"
                                }
                                ],
                        "is_playable": True
                    },
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/5Gu7iDoQjE7anHIbCXckC8"
                            },
                            "href": "https://api.spotify.com/v1/artists/5Gu7iDoQjE7anHIbCXckC8",
                            "id": "5Gu7iDoQjE7anHIbCXckC8",
                            "name": "Vudu Sister",
                            "type": "artist",
                            "uri": "spotify:artist:5Gu7iDoQjE7anHIbCXckC8"
                        }
                    ],
                    "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
                    "disc_number": 1,
                    "duration_ms": 213162,
                    "explicit": False,
                    "external_ids": {
                        "isrc": "usl4r2215515"
                    },
                    "external_urls": {
                        "spotify": "https://open.spotify.com/track/1tWKYNBJh3xKG7qLplCV9z"
                    },
                    "href": "https://api.spotify.com/v1/tracks/1tWKYNBJh3xKG7qLplCV9z",
                    "id": "1tWKYNBJh3xKG7qLplCV9z",
                    "is_playable": True,
                    "name": "Psalms",
                    "popularity": 1,
                    "preview_url": "https://p.scdn.co/mp3-preview/598afd034fd02a35bda732b02e2c22d29ba6f6b2?cid=cfe923b2d660439caf2b557b21f31221",
                    "track_number": 1,
                    "type": "track",
                    "uri": "spotify:track:1tWKYNBJh3xKG7qLplCV9z",
                    "is_local": False
                }
            }
        ]

        self.expected = [
            "spotify:track:0FwjaMc01gWLe9sofzx27J",
            "spotify:track:1tWKYNBJh3xKG7qLplCV9z",
        ]
        self.account._datasets["liked_songs"].expires_at = time() + 999
        self.account._datasets["liked_songs"]._data = self.liked_songs
        self.result = self.account.liked_songs

    def test_name_is_expected_value(self):
        self.assertEqual(self.result, self.expected)
