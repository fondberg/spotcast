# Accounts

Provides a list of Spotify Accounts currently managed by Spotcast.

## Request

```json
{
    "id": 3,
    "type": "spotcast/castdevices"
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/castdevices`

## Response

```json
{
    "id":2,
    "type":"result",
    "success":true,
    "result": {
        "total":2,
        "accounts": [
            {
                "entry_id":"01JDG07KSBTYWZGJSBJ1EW6XEF",
                "spotify_id":"foo",
                "spotify_name":"Foo",
                "is_default":true,
                "country":"CA"
            },
            {
                "entry_id":"01JDG0ZMDFEN2GDPVHV55R0X4P",
                "spotify_id":"bar",
                "spotify_name":"Bar",
                "is_default":false,
                "country":"CA"
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
> Total number of accounts currently managed by Spotcast
> 
> #### `accounts` (list[dict])
> 
> A list of all accounts managed by Spotcast
> 
> > ##### `entry_id` (str)
> > 
> > The identifier of the configuration entry for the account
> > 
> > ##### `spotify_id` (str)
> > 
> > The Spotify Identifier of the account
> > 
> > ##### `spotify_name` (str)
> > 
> > The Display Name for the account in Spotify
> >
> > ##### `is_default` (bool)
> > 
> > `true` if the account is used as the default account for Spotcast services and websocket endpoints
> > 
> > ##### `country` (str)
> > 
> > The [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code of the user's country as set in the user's account profile.
