# Liked Media

Provides a list of liked media (tracks) for a user.

## Request

```json
{
    "id": 7,
    "type": "spotcast/liked_media",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF"
}
```
### `id` (int)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the WebSocket to reach. Must be `spotcast/liked_media`.

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
        "tracks": [
            "spotify:track:3n3Ppam7vgaVa1iaRUc9Lp",
            "spotify:track:6rqhFxbN4uN6t6z2p3xPQK",
            "spotify:track:7gBEnASdyC9XBZf51a0tpn",
            "spotify:track:3nYCh0PbdJ23V2Jp0CzJ8N",
            "spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"
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

#### `total` (int)

The total number of liked media (tracks) retrieved.

#### `account` (str)

The account used in the query.

#### `tracks` (list[str])

List of Spotify URIs of the liked media (tracks) retrieved. Each entry in the list is a string representing a Spotify track URI. Refer to [URI Format](https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids) for details.
