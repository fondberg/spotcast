# Spotcast 
Home Assistant custom component to start Spotify playback on an idle chromecast device

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromcast device and the Spotify playback after the initial start is done in their respective components.
Becasue starting playback using the API requires more powerful token the username and password used for browser login is used.

Used by https://github.com/custom-cards/spotify-card.

Community post: https://community.home-assistant.io/t/spotcast-custom-component-to-start-playback-on-an-idle-chromecast-device/114232

__Now with support for speaker groups, transferring playback to and between chromecast devices and using HA entity id instead of device_name_. 

***This version requires pychromecast version 3.2.2 and is not yet released by home assistant as per 0.94.2, use the master branch of HA, wait for it to be released (PR is merged) or use an older version of this component (no support for groups or transfer playback) found [here](https://github.com/fondberg/spotcast/tree/6ea00c55289fb33b935a0103c29afe4e63fd72e7)***

## Installation


### Get code
On your HA
```
cd /config/custom_components && git clone https://github.com/fondberg/spotcast.git
```


### Configuration
#### Single account
Add the following to your config
```
spotcast:
  username: !secret spotify_username
  password: !secret spotify_password
```
#### Multiple accounts
Add `accounts` dict to the configuration and populate with a list of accounts to 
be able to initiate playback using diffferent accounts than the default.
```

spotcast:
  username: !secret spotify_primary_username
  password: !secret spotify_primary_password
  accounts:
    niklas:
      username: !secret spotify_niklas_username
      password: !secret spotify_niklas_password
    ming:
      username: !secret spotify_ming_username
      password: !secret spotify_ming_password
```

## Call the service

#### start playback on a device with default account
```
{
	"device_name" : "Kök",
	"uri" : "spotify:playlist:37i9dQZF1DX3yvAYDslnv8"
}
```
where 
 - `device_name` is the friendly name of the Chromecast
 - `uri` is the spotify uri, supports all uris including track (limit to one track)

optionally you can specify the `entity_id` of an existing home assistant chromecast mediaplayer like:
```
{
	"entity_id" : "media_player.vardagsrum",
	"uri" : "spotify:playlist:37i9dQZF1DX3yvAYDslnv8"
}
```

### transfer current playback for the account
Omitting `uri` will check if something is playing on any of the accounts devices and transfer the playback to the specified device.
```
{
	"device_name" : "Högtalare uppe"
}
```
or use the parameter `transfer_playback` which will only transfer if something is playing otherwise use the specified `uri`.
```
{
	"device_name" : "MultiRoom",
	"uri" : "spotify:playlist:37i9dQZF1DX3yvAYDslnv8",
	"transfer_playback" : true
}
```
where 
 - `device_name` is the friendly name of the Chromecast
 - `transfer_playback` (optional) true or false, continue ongoing playback on your Chromecast


#### start playback on a device with non default account
```
{
    "account":"niklas",
	"device_name" : "Kök",
	"uri" : "spotify:playlist:37i9dQZF1DX3yvAYDslnv8"
}
```
where 
 - `account` is the name of account key in the accounts dictionary in the configuration
 - `device_name` is the friendly name of the Chromecast
 - `uri` is the spotify uri, supports all uris including track (limit to one track)

## Use the sensor
Sensor name
```
sensor.chromecast_devices
```
Attributes
```
devices_json: [{"name": "Kök", "cast_type": "audio", "model_name": "Google Home", "uuid": "xxxxx", "manufacturer": "Google Inc."}, {"name": "Högtalare uppe", "cast_type": "group", "model_name": "Google Cast Group", "uuid": "xxxx", "manufacturer": "Google Inc."}, {"name": "Vardagsrum", "cast_type": "cast", "model_name": "HK Citation 300", "uuid": "xxxx", "manufacturer": "Harman Kardon"}]

last_update: 2019-05-01T15:27:49.828553+02:00

friendly_name: Chromecast Devices
```

 
 ## Known issues
 It has been reported that updating the sensor takes more than 10s sometimes. 
 This sensor uses `pychromecast` directly and if you don't need the sensor you can safely comment out the registration 
 of the sensor. 
 ```
     # hass.services.register(DOMAIN, 'start', start_casting,
     #                       schema=SERVICE_START_COMMAND_SCHEMA)
 ```
 
 ## Donate
 If you like what I do and want to support me then I love coffee

<a href="https://www.buymeacoffee.com/fondberg" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

 ## Contribute
 Please do
 
 ## License
 Apache 2.0
