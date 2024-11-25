<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/images/logo/white/128.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/images/logo/dark_gray/128.png">
  <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="./assets/images/logo/green/128.png">
</picture>

------------------------------------------------------------------------------

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![spotcast](https://img.shields.io/github/release/fondberg/spotcast.svg?1)](https://github.com/fondberg/spotcast)
![Maintenance](https://img.shields.io/maintenance/yes/2024.svg)

Home Assistant custom component to start Spotify playback on an idle Chromecast or a Spotify Connect device. Meaning you can target automation for chromecast as well as connect devices.

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromecast device and the Spotify playback after the initial start is done in their respective components. Because starting playback using the API requires more powerful token the username and password used for browser login is used.

Used by [Spotify-Card-V2](https://github.com/mikevanes/spotify-card-v2)

## Installation

### HACS

This component is easiest installed using [HACS](https://github.com/custom-components/hacs).

1. First Make sure you have `spotcast` installed through HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=fondberg&repository=spotcast&category=integration)

2. Then, setup an account:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=spotcast)

### Manual installation

1. Copy all files from custom_components/spotcast/ to custom_components/spotcast/ inside your config Home Assistant directory
2. Reboot your Home Assistant.
3. Click the following link to setup an account:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=spotcast)

## Configuration

### Minimum Home Assistant version

Spotcast is compatible with any version since 2024.11.0.

### Official Spotify Integration

> [!NOTE]
> Note that starting with `v5.0.0`, [Home Assistant Spotify Integration](https://www.home-assistant.io/integrations/spotify/) is no longer a requirement **except for Media Browsing**. Click the following link to setup the spotify integration:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=spotify)

### Setup

There are 2 steps for the setup of an account with spotcast

1. **Integration of the OAuth Client Information:** An OAuth client from Spotify must be provided to access your account profile and informations. You can follow the same step as described in the [Home Assistant Spotify Integration](https://www.home-assistant.io/integrations/spotify/).
2. **Integration of the private API credentials:** Spotcast relies on the private Spotify API to link a chromecast device to your spotify account when you are trying to start playback (mimmicking what the Spotify Desktop or Spotify Mobile app are doing). The only known way of connecting to that API is through the use of browser cookies. These can be retrieved by:
    - connecting to [spotify.com](open.spotify.com)
    - opening the developper console
    - pasting the `sp_dc` and `sp_key` in the Home Assistant setup form

> [!TIP]
> See [Obtaining SP_DC and SP_KEY](./docs/config/obtaining_sp_dc_and_sp_key.md) for more details

## Services

The spotcast custom component provides multiple services to the user for different use cases. The services available are as followed (link to full documentation in table):

> [!TIP]
> If you are converting script from pre `v5` services. The closest equivalence to `spotcast.start` is `spotcast.play_media`

| Service Name                                                           | Description                                                                                                                                       |
| :---                                                                  | :---                                                                                                                                              |
| [spotcast.play_media](./docs/services/play_media.md)                   | Starts playback on a Chromecast or Spotify Connect device using the provided uri as context.                                                      |
| [spotcast.play_liked_songs](./docs/services/play_liked_songs.md)       | Starts playback on a Chromecast or Spotify Connect device using the user's saved tracks as context.                                               |
| [spotcast.play_dj](./docs/services/play_dj.md)                         | Starts playback on a Chromecast or Spotify Connect device using the dj feature as context.                                                        |
| [spotcast.play_from_search](./docs/services/play_from_search.md)       | Starts playback on a Chromecast or Spotify Connect device using a search result as a context.                                                     |
| [spotcast.play_category](./docs/services/play_category.md)             | Starts playback on a Chromecast or Spotify Connect device using a random playlist from a Browse Category as context.                              |
| [spotcast.play_custom_context](./docs/services/play_custom_context.md) | Starts playback on a Chromecast or Spotify Connect device using a list of uris as context                                                         |
| [spotcast.transfer_playback](./docs/services/transfer_playback.md)     | Transfers the playback to a different device. Fails and returns an error if there is no active playback or the playback is already on the device. |
| [spotcast.add_to_queue](./docs/services/add_to_queue.md)               | Adds songs the the playback queue. Fails and returns an error if there is no active playback                                                      |
| [spotcast.play_saved_episodes](./docs/services/play_saved_episodes.md) | Plays the list of podcast episodes part of the `Saved Episodes` playlist                                                                          |

### Data

Multiple options originally in the `spotcast.start` service has been moved to the `data` section. Here is a list of common ones. Some service could have additional options. Look at the service definition for more information on them.

| Option     | type                      | default | description                                                                                                        |
| :---:      | :---:                     | :---:   | :---                                                                                                               |
| `position` | `positive_float`          | `0.000` | The position to start playback (in seconds) of where to start the playback of the first item in the context        |
| `offset`   | `positive_int`            | `0`     | The item in the context to start the playback at. The position is zero based and cannot be negative                |
| `volume`   | `int`, `range 0-100`      | `null`  | The percentage (as an integer of the percentage value) to start plaback at. Volume is kept unchanged if `null`     |
| `repeat`   | `track \| context \| off` | `null`  | The repeat mode is kept the same if `null`                                                                         |
| `shuffle`  | `bool`                    | `null`  | Sets the playback to shuffle if `True`. Is kept unchanged if `null`.                                               |
| `limit`    | `positive_int`            | `null`  | sets the maximum amount of items that can be retrieved from a spotify api endpoint. Retrieves all items if `null`. |


## Entitites

Spotcast creates multiple entities for each Spotify accounts.

### Sensors

| example name                        | description                                                                           | states          |
| :---                               | :---                                                                                  | :---:           |
| `sensor.[...]_spotify_profile`      | Reports the profile of the Spotify Account. Provide attributes linked to the account. | `ok\|unknown`   |
| `sensor.[...]_spotify_devices`      | Tracks the number of devices available for the account.                               | `int`           |
| `sensor.[...]_spotify_followers`    | Tracks the number of followers the account has.                                       | `int`           |
| `sensor.[...]_spotify_liked_songs`  | Tracks the number of songs liked by the account.                                      | `int`           |
| `sensor.[...]_spotify_playlists`    | Tracks the number of playlists created by the account.                                | `int`           |
| `sensor.[...]_spotify_account_type` | Diagnostic sensor that reports the type of account connected through spotcast         | `user`          |
| `sensor.[...]_spotify_product`      | Diagnostic sensor that reports the subscription level of the account.                 | `premium\|free` |

### Binary Sensors

| example name                               | description                                                                                 |
| :---                                      | :---                                                                                        |
| `sensor.[...]_is_default_spotcast_account` | Diagnostic sensor that confirm if the account is currently the default account for spotcast |
| `sensor.[...]_spotify_profile_malfunction` | Diagnostic error sensor that turns on when an connection issue happens with the API         |


### Media Players

Spotcast will create `media_player` entities and devices to represent Spotify Connect Devices linked to a Spotcast account. These media players do not implement any functionality and are ment to be used in service call when starting playback on a spotify connect device.

## Websocket API

Spotcast provides multiple websocket API endpoints:

| endpoint                                                   | description                                                                                                                                                                           |
| :---                                                       | :---                                                                                                                                                                                  |
| [`spotcast/accounts`](./docs/websocket/accounts.md)        | Provides a list of accounts linked to spotcast                                                                                                                                        |
| [`spotcast/castdevices`](./docs/websocket/cast_devices.md) | Provides a list of Chromecast devices available in Home Assistant                                                                                                                     |
| [`spotcast/categories`](./docs/websocket/categories.md)    | Provides a list of [Browse categories](https://developer.spotify.com/documentation/web-api/reference/get-a-category) an account has access to                                         |
| [`spotcast/devices`](./docs/websocket/devices.md)          | Provides a list of Spotify Connect Devices available to the account                                                                                                                   |
| [`spotcast/player`](./docs/websocket/player.md)            | Provides the playback state of an account                                                                                                                                             |
| [`spotcast/playlists`](./docs/websocket/playlists.md)      | Provides the list of playlists. Either the user's playlist of the playlists part of a [Browse Category](https://developer.spotify.com/documentation/web-api/reference/get-a-category) |


## Contribute

Please do! Open a Pull Request with your improvements. This project was made possible by the original creator Niklas Fondberg. All improvements are greatly appreciated.

In order for a pull request to be approve, you will have to provide a full test coverage of you code. A pylint score >=9/10 is also required.

## License

Apache 2.0
