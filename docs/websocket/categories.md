# Categories

Provides the list of Browse Categories available for an account.

## Request

```json
{
    "id": 4,
    "type": "spotcast/categories",
    "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
    "limit": 10,
}
```

### `id` (str)

The id of the transaction. Must be an increment of the last transaction id.

### `type` (str)

The endpoint of the websocket to reach. Must be `spotcast/categories`

### `account` (str)

*Optional*

The entry id of the account used to look for Browse Categories. Defaults to the Spotcast default account if not provided.

### `limit` (int)

*Optional*

Limits the number of categories retrieved to the number provided. If absent, retrives all Browse categories available for the account.

## Response

```json
{
    "id": 4,
    "type": "result",
    "success": true,
    "result":
    {
        "total": 10,
        "account": "01JDG07KSBTYWZGJSBJ1EW6XEF",
        "categories":[
            {
                "id":"0JQ5DAt0tbjZptfcdMSKl3",
                "icon":"https://t.scdn.co/images/728ed47fc1674feb95f7ac20236eb6d7.jpeg",
                "name":"Made For You"
            },
            {
                "id":"0JQ5DAqbMKFNNuveavxU1i",
                "icon":"https://t.scdn.co/images/728ed47fc1674feb95f7ac20236eb6d7.jpeg",
                "name":"New Releases"
            },
            {
                "id":"0JQ5DAtOnAEpjOgUKwXyxj",
                "icon":"https://t.scdn.co/images/728ed47fc1674feb95f7ac20236eb6d7.jpeg",
                "name":"Discover"
            },
            ...
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
> #### `account` (str)
>
> The id of the account used in the query
> 
> #### `categories` (list[dict])
> 
> The list of browse categories retrieved
>
> > ##### `id` (str)
> > 
> > The identifier of the Browse category
> > 
> > ##### `icon` (str)
> > 
> > URL to the image used for the browse category in Spotify's Apps
> > 
> > ##### `name` (str)
> > 
> > The name of the Browse Category
