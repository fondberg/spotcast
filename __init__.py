import logging
import voluptuous as vol

from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_PASSWORD, CONF_USERNAME)

DOMAIN = 'spotcast'
_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME = 'device_name'
CONF_SPOTIFY_URI = 'uri'

SERVICE_START_COMMAND_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_NAME): cv.string,
    vol.Required(CONF_SPOTIFY_URI): cv.string
})

def setup(hass, config):
    """Setup the Spotcast service."""

    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]

    # sensor
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    # service
    def get_chromecast_devices():
        import pychromecast
        
        chromecasts = pychromecast.get_chromecasts()
        if chromecasts == None:
            raise HomeAssistantError('Could not find any Chromecast devices')
        else:
            return chromecasts

    def get_spotify_token(username, password):
        import spotify_token as st
        import time
        data = st.start_session(username, password)
        access_token = data[0]
        expires = data[1] - int(time.time())
        return access_token, expires

    def play(client, spotify_device_id, uri):
        _LOGGER.debug('Got uri: %s', uri)
        if uri.find("track") > 0:
            client.start_playback(device_id=spotify_device_id, uris=[uri])
        else:
            client.start_playback(device_id=spotify_device_id, context_uri=uri)

    def start_casting(call):
        """service called."""

        from pychromecast.controllers.spotify import SpotifyController
        import spotipy

        uri = call.data.get(CONF_SPOTIFY_URI)
        device_name = call.data.get(CONF_DEVICE_NAME)
        # Find chromecast device
        chromecasts = get_chromecast_devices()
        # login as real browser to get powerful token
        access_token, expires = get_spotify_token(username=username, password=password)
        client = spotipy.Spotify(auth=access_token)
        sp = SpotifyController(access_token, expires)        
        
        group = None

        for _device in chromecasts:
            _device.wait()
            if _device.name == device_name:
                _device.register_handler(sp)
                sp.launch_app()
                if _device.cast_type == 'group':
                    group = True
                else:
                    group = False
                
        if group == True:
          for _app in chromecasts:
              if _app.app_id == '531A4F84':
                master_device = _app.name
        else:
            master_device = device_name

        spotify_device_id = None
        devices_available = client.devices()
        for device in devices_available['devices']:
            if device['name'] == master_device:
                spotify_device_id = device['id']
                break

        play(client, spotify_device_id, uri)

    hass.services.register(DOMAIN, 'start', start_casting,
                           schema=SERVICE_START_COMMAND_SCHEMA)

    return True
