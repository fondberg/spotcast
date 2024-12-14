# Tracks

Provides the list of tracks from a specified playlist.

## Request

```json
{
    "id": 15,
    "type": "spotcast/tracks",
    "playlist_id": "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF"
}
```
### `id` (int)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the WebSocket to reach. Must be `spotcast/tracks`.

### `playlist_id` (str)

The Spotify ID or URI of the playlist whose tracks are to be retrieved. This can be a full URI such as `spotify:playlist:37i9dQZF1DXcBWIGoYBM5M` or just the playlist ID (`37i9dQZF1DXcBWIGoYBM5M`).

### `account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.

## Response
```json
{
    "id": 15,
    "type": "result",
    "result": {
        "total": 2,
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "tracks": [
            {
                "id": "5J7j5w4UUMnGJ21rYVQfob",
                "name": "The Nights",
                "uri": "spotify:track:5J7j5w4UUMnGJ21rYVQfob",
                "album": {...},
                "artists": [
                    {...},
                    {...}
                ]
            },
            {...},
            {...}
        ]
    }
}
```
### `id` (int)

The id provided in the request.

### `type` (str)

Always `result` on a successful request.

### `result` (dict)

The result of the transaction.

> #### `total` (int)
>
> The total number of tracks retrieved.
>
> #### `account` (str)
>
> The account used in the query.
>
> #### `tracks` (list[dict])
>
> List of tracks retrieved from the specified playlist. Each track includes:
>
> > ##### `id` (str)
> > 
> > Spotify's unique ID for the track.
> > 
> > ##### `name` (str)
> > 
> > The name of the track.
> > 
> > ##### `uri` (str)
> > 
> > Spotify URI for the track. Refer to [URI Format](https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids) for details.
> > 
> > ##### `album` (dict)
> > 
> > Information about the album the track belongs to. Refer to [Get playlist tracks](https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks) for details.
> > 
> > ##### `artists` (list[dict])
> > 
> > List of artists who contributed to the track. Refer to [Get playlist tracks](https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks) for details.

