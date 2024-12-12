# Like Media

Like a list of Spotify URIs for a specific Spotify account.

## Action

```yaml
action: spotcast.like_media
data:
    spotify_uris:
        - spotify:track:1yuxSH79Cj1nGqN1AKD9p5
        - spotify:track:2dbJ0mn0vTVz6mc3rk2t77
    account: 01JDG07KSBTYWZGJSBJ1EW6XEF
```
### `spotify_uris` (list of str)

A list of Spotify URIs or URLs to be liked. These can represent various types of content, including tracks, albums, or playlists.

### `account` (str)

*Optional*

The `entry_id` of the account to use for Spotcast. If empty, the default Spotcast account is used.
