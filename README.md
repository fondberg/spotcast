# Spotcast 
Home Assistant custom component to start Spotify playback on an idle chromecast device

This component is not meant to be a full Spotify chromecast media_player but only serves to start the playback. Controlling the chromcast device and the Spotify playback after the initial start is done in their respective components.


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
  username: !secret spotify_primary_password
  password: !secret spotify_primary_password
  accounts:
    niklas:
      username: !secret spotify_niklas_password
      password: !secret spotify_niklas_password
    ming:
      username: !secret spotify_ming_password
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


 
 ## Known issues
 It doesn't seem to be possible to start playback on a Google Home Chromecast speaker group for some unknown reason.
 
 
 ## Contribute
 Please do
 
 ## License
 Apache 2.0