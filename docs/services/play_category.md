# Playlist from Category

`spotcast.play_category`

## Description

Play a random playlist from a Spotify Browse Category

## Example service call

```yaml
action: spotcast.play_category
data:
    media_player:
        entity_id: media_player.foo
    category: "Made for You"
    spotify_account: 01JDG07KSBTYWZGJSBJ1EW6XEF
    data:
        limit: 10
```

## Fields

### Media Player

Let the user select a compatible device on which to start the playback. **_Must be a single device_**.

### Category

Can be either the name of a Browse Category or a Category ID. In the case of a Category Name, a fuzzy match is applied to match the best case for the category name. A category ID must be exact. You can find a list of Categories by calling the [`spotcast/categories` Websocket Endpoint](../websocket/categories.md).

### Spotify Account

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.

### Data

*Optional*

Set of additional settings to apply when starting the playback. The available options are:

| Option     | type                      | default | description                                                                                                                                 |
| :---:      | :---:                     | :---:   | :---                                                                                                                                        |
| `position` | `positive_float`          | `0.000` | The position to start playback (in seconds) of where to start the playback of the first item in the context                                 |
| `offset`   | `positive_int`            | `0`     | The item in the context to start the playback at. The position is zero based and cannot be negative. Is ingored in the case of a track URI. |
| `volume`   | `int`, `range 0-100`      | `null`  | The percentage (as an integer of the percentage value) to start plaback at. Volume is kept unchanged if `null`                              |
| `repeat`   | `track \| context \| off` | `null`  | The repeat mode is kept the same if `null`                                                                                                  |
| `shuffle`  | `bool`                    | `null`  | Sets the playback to shuffle if `True`. Is kept unchanged if `null`.                                                                        |
| `limit`    | `possite_int`             | `null`  | Sets the maximum number of categories to retrieve. Retrieves all categories if `null`.                                                      |
