# Add To Queue

Adds a list of spotify URI to the 

## Action

```yaml
action: spotcast.add_to_queue
data:
    spotify_uris:
        - spotify:track:03Vh87Tg6boENhCNstwKX2
        - spotify:track:2GfQhXyoUXYTkMHDXJhCU5
    spotify_account: 01JDG07KSBTYWZGJSBJ1EW6XEF
```

###  `spotify_uris` (list[str])

A list of spotify URI or URL to add to the queue of the current playback

### `spotify_account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.
