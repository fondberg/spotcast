# Accounts

`spotcast/accounts`

## Description

Provides a list of account managed by Spotcast.

## Example

```json
{
    "id": 2,
    "type": "spotcast/accounts"
}
```

## Fields

- `id(int)`: The id of the current transaction. Must be an increment of the last transaction.
- `type(str)`: The endpoint to reach. Must be `spotcast/accounts`

## Reply

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
