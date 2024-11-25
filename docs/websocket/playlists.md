# Playlists

Provides a list of playlists based on a Browse categories

## Request

```json
{
    "id": 7,
    "type": "spotcast/playlists",
    "category": "metal",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
    "limit": 20
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/categories`

### `category` (str)

A Browse category in Spotify. Can be a category name, id, or `user` to retrieve user's playlists

### `account` (str)

*Optional*

The entry id of the account used to get the active playback state. Defaults to the default spotcast account if not provided.

### `limit` (int)

*Optional*

Sets a limit to the number of playlists to retrieve in a category

## Response

```json
{
    "id": 7,
    "type": "result",
    "result": {
        "total": 20,
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "category": "0JQ5DAqbMKFDkd668ypn6O",
        "playlists": [
            {...},
            {...}
        ]
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

The result of the transaction

> #### `total` (int)
> 
> The total number of playlists retrieved
>
> #### `account` (str)
>
> The account used in the query
>
> #### `category` (str)
>
> The id of the category used in the query
> 
> #### `playlists` (list[dict])
> 
> List of the playlists retrieved that are part of the requested category. See [Get Playlist](https://developer.spotify.com/documentation/web-api/reference/get-playlist) for details about the fields
