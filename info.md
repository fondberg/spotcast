<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/images/logo/white/h64.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/images/logo/dark_gray/h64.png">
  <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="./assets/images/logo/dark_gray/h64.png">
</picture>

------------------------------------------------------------------------------

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![spotcast](https://img.shields.io/github/release/fondberg/spotcast.svg?1)](https://github.com/fondberg/spotcast)
![Maintenance](https://img.shields.io/maintenance/yes/2024.svg)

Home Assistant custom component to start Spotify playback on an idle Chromecast or a Spotify Connect device. Meaning you can target automation for chromecast as well as connect devices.

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromecast device and the Spotify playback after the initial start is done in their respective components. Because starting playback using the API requires more powerful token the username and password used for browser login is used.

## Component configuration

Once the component has been installed, you need to configure it using the web interface. You can either click on the link or follow the instructions bellow:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=spotcast)

1. Go to `Settings->Devices & Services`
2. Click `+ Add Integration`
3. Search for Spotcast
4. Select the integration and follow the instructions

For full configuration documentation, see [README](https://github.com/fondberg/spotcast)
