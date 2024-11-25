# Player

Provides the active playback state for a Spotify Account

## Request

```json
{
    "id": 6,
    "type": "spotcast/player",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF"
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/categories`

### `account` (str)

*Optional*

The entry id of the account used to get the active playback state. Defaults to the default spotcast account if not provided.

## Response

```json
{
    "id": 6,
    "type": "result",
    "result": {
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "state" : {
        "device": {
            "id": "12345",
            "is_active": true,
            "is_private_session": false,
            "is_restricted": false,
            "name": "foo",
            "type": "Computer",
            "volume_percent": 100,
            "supports_volume": true
        },
        "repeat_state": "context",
        "shuffle_state": false,
        "context": {
            "type": "album",
            "href": "https://api.spotify.com/v1/albums/1chw1DFmefTueG1VbNVoGN",
            "external_urls": {
                "spotify": "https://open.spotify.com/album/1chw1DFmefTueG1VbNVoGN"
            },
            "uri": "spotify:album:1chw1DFmefTueG1VbNVoGN"
        },
        "timestamp": 1732541310670,
        "progress_ms": 76425,
        "is_playing": true,
        "item": {
            "album": {
                "album_type": "album",
                "total_tracks": 14,
                "external_urls": {
                    "spotify": "https://open.spotify.com/album/1chw1DFmefTueG1VbNVoGN"
                },
                "href": "https://api.spotify.com/v1/albums/1chw1DFmefTueG1VbNVoGN",
                "id": "1chw1DFmefTueG1VbNVoGN",
                "images": [
                    {
                        "url": "https://i.scdn.co/image/ab67616d0000b273d365d1c5923d54a868996ce8",
                        "height": 640,
                        "width": 640
                    },
                    {
                        "url": "https://i.scdn.co/image/ab67616d00001e02d365d1c5923d54a868996ce8",
                        "height": 300,
                        "width": 300
                    },
                    {
                        "url": "https://i.scdn.co/image/ab67616d00004851d365d1c5923d54a868996ce8",
                        "height": 64,
                        "width": 64
                    }
                ],
                "name": "GREIF",
                "release_date": "2024-08-23",
                "release_date_precision": "day",
                "type": "album",
                "uri": "spotify:album:1chw1DFmefTueG1VbNVoGN",
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/6yCjbLFZ9qAnWfsy9ujm5Y"
                        },
                        "href": "https://api.spotify.com/v1/artists/6yCjbLFZ9qAnWfsy9ujm5Y",
                        "id": "6yCjbLFZ9qAnWfsy9ujm5Y",
                        "name": "Zeal & Ardor",
                        "type": "artist",
                        "uri": "spotify:artist:6yCjbLFZ9qAnWfsy9ujm5Y"
                    }
                ],
                "is_playable": true
            },
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6yCjbLFZ9qAnWfsy9ujm5Y"
                    },
                    "href": "https://api.spotify.com/v1/artists/6yCjbLFZ9qAnWfsy9ujm5Y",
                    "id": "6yCjbLFZ9qAnWfsy9ujm5Y",
                    "name": "Zeal & Ardor",
                    "type": "artist",
                    "uri": "spotify:artist:6yCjbLFZ9qAnWfsy9ujm5Y"
                }
            ],
            "disc_number": 1,
            "duration_ms": 231813,
            "explicit": false,
            "external_ids": {
                "isrc": "QM4TW2489136"
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/track/1Yk1xHfMPC43JQ5R8JO6Ia"
            },
            "href": "https://api.spotify.com/v1/tracks/1Yk1xHfMPC43JQ5R8JO6Ia",
            "id": "1Yk1xHfMPC43JQ5R8JO6Ia",
            "is_playable": true,
            "name": "Fend You Off",
            "popularity": 41,
            "preview_url": "https://p.scdn.co/mp3-preview/8a04fe6a20961f18c01eb8b85ca390873764efa0?cid=cfe923b2d660439caf2b557b21f31221",
            "track_number": 2,
            "type": "track",
            "uri": "spotify:track:1Yk1xHfMPC43JQ5R8JO6Ia",
            "is_local": false
        },
        "currently_playing_type": "track",
        "actions": {
            "disallows": {
                "resuming": true
            }
        },
        "smart_shuffle": false
    }
}
```

### `id` (str)

The id provided in the request

### `type` (str)

Always `result` on a successful request.

### `success` (bool)

True if the transaction was successful.

### `result` (dict)

The result of the query.

> #### `account` (str)
>
> The account used in the query
>
> #### `state` (dict)
>
> The current playback state. See the [API documentation](https://developer.spotify.com/documentation/web-api/reference/get-information-about-the-users-current-playback) for details of the fields. If no active playback. Returns an empty dictionary.
