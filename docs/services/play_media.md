# Play Media

Play spotify media on Spotcast compatible device

## Action

```yaml
action: spotcast.play_media
data:
    media_player:
        entity_id: media_player.foo
    spotify_uri: spotify:album:1chw1DFmefTueG1VbNVoGN
    spotify_account: 01JDG07KSBTYWZGJSBJ1EW6XEF
    data:
        repeat: context
```

### `media_player` (dict)

Let the user select a compatible device on which to start the playback. **_Must be a single device_**.

### `uri` (str)

The Spotify URI or URL used for the context in the playback. In the case of a track URI, the context will become the album of the track, but set to the correct position of the track in the album.

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
