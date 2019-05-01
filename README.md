# Spotcast 
Home Assistant custom component to start Spotify playback on an idle chromecast device

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromcast device and the Spotify playback after the initial start is done in their respective components.

Used by https://github.com/custom-cards/spotify-card.

Community post: https://community.home-assistant.io/t/spotcast-custom-component-to-start-playback-on-an-idle-chromecast-device/114232

## Installation


### Get code
On your HA
```
cd /config/custom_components && git clone https://github.com/fondberg/spotcast.git
```


### Configuration
Add the following to your config
```
spotcast:
  username: !secret spotify_username
  password: !secret spotify_password
```


## Call the service
```
{
	"device_name" : "Kök",
	"uri" : "spotify:playlist:37i9dQZF1DX3yvAYDslnv8"
}
```
where 
 - `device_name` is the friendly name of the Chromecast
 - `uri` is the spotify uri, supports all uris including track (limit to one track)
 
 ## Known issues
 It doesn't seem to be possible to start playback on a Google Home Chromecast speaker group for some unknown reason.
 
 
 ## Contribute
 Please do
 
 ## License
 Apache 2.0
