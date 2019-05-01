# Spotcast 
Home Assistant custom component to start Spotify playback on an idle chromecast device

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromcast device and the Spotify playback after the initial start is done in their respective components.
Becasue starting playback using the API requires more powerful token the username and password used for browser login is used.

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
 
## Use the sensor
Sensor name
```
sensor.chromecast_devices
```
Attributes
```
devices_json: [{"name": "Kök", "cast_type": "audio", "model_name": "Google Home", "uuid": "fa4dda80-24b6-36eb-450c-a54f021a264a", "manufacturer": "Google Inc."}, {"name": "Högtalare uppe", "cast_type": "group", "model_name": "Google Cast Group", "uuid": "6f79c59c-f7af-4790-a0d2-c0cbf52ed71d", "manufacturer": "Google Inc."}, {"name": "Vardagsrum", "cast_type": "cast", "model_name": "HK Citation 300", "uuid": "89799911-c4bd-a97c-ef5d-1c3d95d83e81", "manufacturer": "Harman Kardon"}]

last_update: 2019-05-01T15:27:49.828553+02:00

friendly_name: Chromecast Devices
```
 
 ## Known issues
 It doesn't seem to be possible to start playback on a Google Home Chromecast speaker group for some unknown reason. Probably due to missing functionality in https://github.com/balloob/pychromecast
 
 
 ## Contribute
 Please do
 
 ## License
 Apache 2.0
