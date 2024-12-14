# Search

Search for playlists or tracks based on a query.

## Request

```json
{
    "id": 7,
    "type": "spotcast/search",
    "query": "rock",
    "search_type": "playlist",
    "limit": 10,
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF"
}
```
### `id` (int)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the WebSocket to reach. Must be `spotcast/search`.

### `query` (str)

The search query string. This can be any term, such as a track name, album, artist, playlist name, or genre.

### `searchType` (str)

*Optional*

The type of search. Can be `playlist`, `track`, `album`, or `artist`. Defaults to `playlist` if not specified.

### `limit` (int)

*Optional*

Sets a limit to the number of results to retrieve. Defaults to 10 if not specified.

### `account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.

## Response
```json
{
    "id": 7,
    "type": "result",
    "result": {
        "total": 5,
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "playlists": [
            {
                "id": "37i9dQZF1DXcBWIGoYBM5M",
                "name": "Rock Classics",
                "uri": "spotify:playlist:37i9dQZF1DXcBWIGoYBM5M",
                "description": "Classic rock hits",
                "icon": "https://link_to_image.com"
            },
            {
                "id": "37i9dQZF1DX4UtD7rx6U8w",
                "name": "Indie Rock",
                "uri": "spotify:playlist:37i9dQZF1DX4UtD7rx6U8w",
                "description": "Indie rock tracks",
                "icon": "https://link_to_image.com"
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
> The total number of results retrieved.
> 
> #### `account` (str)
> 
> The account used in the query.
> 
> #### `playlists` (list[dict])
> 
> A list of search results based on the search type. The key name will change depending on the search type and could be `playlists`, `tracks`, `albums`, or `artists`.
> 
> > ##### `id` (str)
> > 
> > The unique ID for the result. For playlists, this will be the Spotify playlist ID. For tracks, it will be the Spotify track ID. For albums or artists, it will be the corresponding Spotify ID.
> > 
> > ##### `name` (str)
> > 
> > The name of the playlist, track, album, or artist.
> > 
> > ##### `uri` (str)
> > 
> > The Spotify URI for the playlist, track, album, or artist. Refer to [URI Format](https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids) for details.
> > 
> > ##### `description` (str)
> > 
> > A description of the playlist, track, album, or artist, if available.
> > 
> > ##### `icon` (str)
> > 
> > A URL to an image associated with the playlist, track, album, or artist, if available.

