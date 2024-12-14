# View Playlists

Provides a list of playlists from a specific view.
## Request

```json
{
    "id": 10,
    "type": "spotcast/view",
    "name": "recently-played",
    "account": "john",
    "limit": 20,
    "language": "en"
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/view`

### `name` (str)

### `name` (str)

The name of the view to retrieve playlists for. This could represent different types of views, including **featured**, **recently-played** and **Discover Weekly**. You can view all available options in the Spotify API (token needed) [here](https://api.spotify.com/v1/views/personalized-recommendations).

### `account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.

### `limit` (int)

*Optional*

Sets a limit on the number of playlists to retrieve. Defaults to the maximum allowed if not specified.

### `language` (str)

*Optional*

Specifies the preferred language for the response. Must be a 2-character language code (e.g., `"en"` for English).

## Response
```json
{
    "id": 7,
    "type": "result",
    "result": {
        "total": 2,
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "playlists": [
            {
                "id": "37i9dQZF1DXcBWIGoYBM5M",
                "name": "Today's Top Hits",
                "uri": "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
                "description": "The biggest songs in the world. Cover: Olivia Rodrigo",
                "icon": "https://i.scdn.co/image/ab67706f0000000261e3d43c22d7b7f74c8a85e8"
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
> The total number of playlists retrieved.
>
> #### `account` (str)
>
> The account used in the query.
>
> #### `playlists` (list[dict])
>
> List of playlists retrieved based on the specified view. Each playlist includes:
>
> > ##### `id` (str)
> > 
> > Spotify's unique ID for the playlist.
> > 
> > ##### `name` (str)
> > 
> > The name of the playlist.
> > 
> > ##### `uri` (str)
> > 
> > Spotify URI for the playlist. Refer to [URI Format](https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids) for details.
> > 
> > ##### `description` (str)
> > 
> > A short description of the playlist.
> > 
> > ##### `icon` (str)
> > 
> > A URL to the playlist's icon or image.