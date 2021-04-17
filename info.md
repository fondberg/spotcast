[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![spotcast](https://img.shields.io/github/release/fondberg/spotcast.svg?1)](https://github.com/fondberg/spotcast) ![Maintenance](https://img.shields.io/maintenance/yes/2021.svg)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&message=🥨&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://www.buymeacoffee.com/fondberg)

# Spotcast
Home Assistant custom component to start Spotify playback on an idle chromecast device or a Spotify Connect device.

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromecast device and the Spotify playback after the initial start is done in their respective components.
Because starting playback using the API requires more powerful token the username and password used for browser login is used.

Used by https://github.com/custom-cards/spotify-card.

# Minimal Configuration
Note that since v3.5.2 you must also have the official [Home Assistant Spotify Integration](https://www.home-assistant.io/integrations/spotify/) installed and configured for this custom component to work. This is because it provides the correct device list which has the correct scopes in its token.

### Single account
Add the following to your config
```yaml
spotcast:
  sp_dc: !secret sp_dc
  sp_key: !secret sp_key
```

For full configuration documentation and information on how to obtain the correct `sp_dc` and `sp_key` values, see [README](https://github.com/fondberg/spotcast)
