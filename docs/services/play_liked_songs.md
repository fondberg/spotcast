# Play Liked Songs

Play user's liked songs

## Action

```yaml
action: spotcast.play_liked_songs
data:
    media_player:
        entity_id: media_player.foo
    spotify_account: 01JDG07KSBTYWZGJSBJ1EW6XEF
    data:
        repeat: context
```

### `media_player` (dict)

Let the user select a compatible device on which to start the playback. **_Must be a single device_**.

### `spotify_account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.

### `data` (dict)

*Optional*

Set of additional settings to apply when starting the playback. The available options are:

| Option     | type                      | default | description                                                                                                                                 |
| :---:      | :---:                     | :---:   | :---                                                                                                                                        |
| `position` | `positive_float`          | `0.000` | The position to start playback (in seconds) of where to start the playback of the first item in the context                                 |
| `offset`   | `positive_int`            | `0`     | The item in the context to start the playback at. The position is zero based and cannot be negative. Is ingored in the case of a track URI. |
| `volume`   | `int`, `range 0-100`      | `null`  | The percentage (as an integer of the percentage value) to start plaback at. Volume is kept unchanged if `null`                              |
| `repeat`   | `track \| context \| off` | `null`  | The repeat mode is kept the same if `null`                                                                                                  |
| `shuffle`  | `bool`                    | `null`  | Sets the playback to shuffle if `True`. Is kept unchanged if `null`.                                                                        |
| `random`   | `bool`                    | `False` | Sets the first played song to a random one of the account's liked songs                                                                     |
