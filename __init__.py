import logging
import voluptuous as vol
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_PASSWORD, CONF_USERNAME)

DOMAIN = "spotcast"
_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME = "device_name"
CONF_SPOTIFY_URI = "uri"

SERVICE_START_COMMAND_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_NAME): cv.string,
    vol.Required(CONF_SPOTIFY_URI): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
})

def setup(hass, config):
    """Setup the Spotcast service."""

    def get_chromcase_device(device_name):
        import pychromecast
        chromecasts = pychromecast.get_chromecasts()
        cast = None
        for _cast in chromecasts:
            print("Found cast: %s" % _cast.name )
            if _cast.name == device_name:
                cast = _cast
                return cast
        if cast == None:
            raise HomeAssistantError("Could not find device with name {}".format(device_name))


    def get_spotify_token(username, password):
        import spotify_token as st
        import time
        data = st.start_session(username, password)
        access_token = data[0]
        expires = data[1] - int(time.time())
        return access_token, expires

    def play(client, spotify_device_id, uri):
        print("Starting playback on %s " % spotify_device_id)
        _LOGGER.info('Got uri: %s', uri)
        # client.start_playback(device_id=spotify_device_id, uris=["spotify:track:3Zwu2K0Qa5sT6teCCHPShP"])
        # client.start_playback(device_id=spotify_device_id, context_uri="spotify:playlist:5zWx4nzIkTxHM5fPS6MHnJ")
        client.start_playback(device_id=spotify_device_id, context_uri=uri)

    def start_casting(call):
        """service called."""

        from pychromecast.controllers.spotify import SpotifyController
        import spotipy

        uri = call.data.get(CONF_SPOTIFY_URI)
        user = call.data.get(CONF_USERNAME)
        password = call.data.get(CONF_PASSWORD)
        device_name = call.data.get(CONF_DEVICE_NAME)

        # Find chromecast device
        cast = get_chromcase_device(device_name)
        cast.wait()

        # login as real browser to get powerful token
        access_token, expires = get_spotify_token(username=user, password=password)

        client = spotipy.Spotify(auth=access_token)

        # launch the app on chromecast
        sp = SpotifyController(access_token, expires)
        cast.register_handler(sp)
        sp.launch_app()

        spotify_device_id = None
        devices_available = client.devices()
        for device in devices_available['devices']:
            if device['name'] == device_name:
                print("Found it! device %s " % device['name'])
                spotify_device_id = device['id']
                break

        play(client, spotify_device_id, uri)

    hass.services.register(DOMAIN, 'start', start_casting,
                           schema=SERVICE_START_COMMAND_SCHEMA)

    return True


# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# def start_playback(uri, access_token):
#     websession = async_get_clientsession(hass)
#     with async_timeout.timeout(15, loop=hass.loop):
#         req = await websession.put(
#             cloud.google_actions_sync_url, headers={
#                 "Authorization": "Bearer {}".format(access_token),
#                 "Content-Type": 'application/json'
#             })
