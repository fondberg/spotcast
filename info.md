[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![spotcast](https://img.shields.io/github/release/fondberg/spotcast.svg?1)](https://github.com/fondberg/spotcast) ![Maintenance](https://img.shields.io/maintenance/yes/2020.svg)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&message=🥨&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://www.buymeacoffee.com/fondberg)

## right now defunct due to https://github.com/enriquegh/spotify-webplayer-token/issues/6


# Spotcast 
Home Assistant custom component to start Spotify playback on an idle chromecast device

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromcast device and the Spotify playback after the initial start is done in their respective components.
Becasue starting playback using the API requires more powerful token the username and password used for browser login is used.

Used by https://github.com/custom-cards/spotify-card.

***Required configuration change with release 2.9.0:***

***The parameter transfer_playback does not exist anymore and if you use it, you need to update your configuration. Use an empty uri and optionally the new parameter force_playback instead.***

# Minimal Configuration
#### Single account
Add the following to your config
```
spotcast:
  username: !secret spotify_username
  password: !secret spotify_password
```

For full configuration documentation see [README](https://github.com/fondberg/spotcast)
