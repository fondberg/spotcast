# Devices

Provides the list of currently available player for a Spotify Account

## Request

```json
{
    "id": 4,
    "type": "spotcast/devices",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF"
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/categories`

### `acount` (str)

*Optional*

The entry id of the account used to look for Browse Categories. Defaults to the Spotcast default account if not provided.

```json
{
    "id": 6,
    "type": "result",
    "success": true,
    "result": {
        "total": 1,
        "devices": [
            {
                "id":"042ee68e1c57247fe3c214f1669e5a4933a9f6b4",
                "is_active": false,
                "is_private_session": false,
                "is_restricted": false,
                "name": "billabongvalley",
                "supports_volume": true,
                "type": "Computer",
                "volume_percent": 53
            }
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
> Number of browse categories retrieved
> 
> #### `devices` (list[dict])
> 
> The number of player available for the account at the moment of the transaction
>
> > ##### `id` (str)
> > 
> > The Spotify ID of the device
> > 
> > ##### `is_active` (bool)
> > 
> > `true` if the device is actively playing media
> > 
> > ##### `is_private_session` (bool)
> > 
> > `true` if the device is currently set to a private session
> > 
> > ##### `is_restricted` (bool)
> > 
> > `true` if the device can,t be controlled through API calls (meaning Spotcast) cannot control the device
> > 
> > ##### `name` (str)
> > 
> > Name of the device as presented in Spotify's Apps
> > 
> > ##### `supports_volume` (bool)
> > 
> > `true` if the device's volume can be controlled through the API
> > 
> > ##### `type` (str)
> > 
> > The type of devices the media player is
> > 
> > ##### `volume_percent` (int)
> > 
> > An integer between `0` and `100` representing the percentage the voume is set at.
