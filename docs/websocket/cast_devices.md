# Cast Devices

Provides a list of Chromecast Devices available in Home Assistant.

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
    "id":3,
    "type":"result",
    "success":true,
    "result": {
        "total":13,
        "devices": [
            {
                "entity_id":"media_player.reveil",
                "uuid":"",
                "model_name":"Lenovo Smart Clock",
                "friendly_name":"Réveil",
                "manufacturer":"LENOVO"
            },
            {
                "entity_id":"media_player.cuisine",
                "uuid":"",
                "model_name":"Google Home",
                "friendly_name":"Cuisine",
                "manufacturer":"Google Inc."
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
> Number of Chromecast Devices Available in Home Assistant
> 
> #### `devices` (list[dict])
> 
> A list of Chromecast devices
> 
> > ##### `entity_id` (str)
> > 
> > The entity id of the device in Home Assistant
> > 
> > ##### `uuid` (str)
> > 
> > The Universal Unique Identifier of the Chromecast device
> > 
> > ##### `model_name` (str)
> > 
> > The model of the Chromecast Device as reported by itself.
> > 
> > ##### `friendly_name` (str)
> > 
> > Name of the device in Google Services
> > 
> > ##### `manufacturer` (str)
> > 
> > The manufacturer of the Chromecast Device as reported by itself.
