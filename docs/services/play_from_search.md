# Play From Search

Starts playing the top result of a search in Spotify. Either starts playing the top item or a list of top item in the case of tracks.

## Action

```yaml
action: spotcast.play_from_search
data:
    media_player:
        entity_id: media_player.foo
    search_term: Taman Shud
    item_types:
        - track
    filters:
        artist: The Drones
        album: Feelin Kinda Free
        year: 2010-2019
    spotify_account: 01JDG07KSBTYWZGJSBJ1EW6XEF
    data:
        repeat: context
```

### `media_player` (dict)

Let the user select a compatible device on which to start the playback. **_Must be a single device_**.

### `search_term` (str)

A generic search term that could be for any type of items

### item_types (list[str])

A list of item types to look for in the search query.

### `tags` (list[str])

*optional*

A list of tags used to limit the search. Can only be used to search for albums:

- `hipster`: Limits results to albums with a popularity of less than 10%
- `new`: Limits results to albums released in the past 2 weeks

### `filters` (dict[str,str])

A list of filters to apply to the search result. Are key value pairs of filters that can be:

- `album`: The name of the album the item searched for is on. Can only be used on tracks or album
- `artist`: The name of the artist that made the item searched.
- `track`: The name of the track searched for. Can only be used on tracks
- `year`: The year the item was created. Can be a specific date like `2016` or a range like `2010-2019`
- `upc`: The UPC code of the album searched for. Can only be used with albums
- `isrc`: The Iternational Standard Recording Code of the song searched for. Can only be used on songs.
- `genre`: The genre of the item searched for. can only be used on artist or tracks

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
| `limit`    | `positive_int`            | `20`    | Sets the maximum number of items to retrieve when looking for a track. Forced to 1 for other item types                                     |
