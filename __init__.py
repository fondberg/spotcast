import logging
import voluptuous as vol
from homeassistant.util import slugify
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_PASSWORD, CONF_USERNAME, STATE_PLAYING)

_VERSION = '1.1.0'
DOMAIN = 'spotcast'

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME = 'device_name'
CONF_SPOTIFY_URI = 'uri'
CONF_ACCOUNTS = 'accounts'
CONF_SPOTIFY_ACCOUNT = 'account'

SERVICE_START_COMMAND_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_NAME): cv.string,
    vol.Required(CONF_SPOTIFY_URI): cv.string,
    vol.Optional(CONF_SPOTIFY_ACCOUNT): cv.string

})

ACCOUNTS_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_ACCOUNTS): cv.schema_with_slug_keys(ACCOUNTS_SCHEMA),
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Setup the Spotcast service."""
    conf = config[DOMAIN]

    username = conf[CONF_USERNAME]
    password = conf[CONF_PASSWORD]
    accounts = conf.get(CONF_ACCOUNTS)

    hass.data[DOMAIN] = {
        'chromecasts': []
    }

    # sensor
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    # service
    def get_chromcase_device(device_name):
        import pychromecast
        chromecasts = pychromecast.get_chromecasts()
        cast = None
        for _cast in chromecasts:
            if _cast.name == device_name:
                cast = _cast
                return cast
        if cast == None:
            raise HomeAssistantError('Could not find device with name {}'.format(device_name))


    def get_spotify_token(username, password):
        import spotify_token as st
        import time
        data = st.start_session(username, password)
        access_token = data[0]
        expires = data[1] - int(time.time())
        return access_token, expires

    def play(client, spotify_device_id, uri):
        _LOGGER.debug('Playing URI: %s on device-id: %s', uri, spotify_device_id)
        if uri.find('track') > 0:
            _LOGGER.debug('Playing track using uris= for uri: %s', uri)
            client.start_playback(device_id=spotify_device_id, uris=[uri])
        else:
            _LOGGER.debug('Playing context uri using context_uri for uri: %s', uri)
            client.start_playback(device_id=spotify_device_id, context_uri=uri)

    def transfer_pb(client, spotify_device_id):
        _LOGGER.debug('Transfering playback')
        client.transfer_playback(device_id=spotify_device_id, force_play = True)

    def start_casting(call):
        """service called."""

        from pychromecast.controllers.spotify import SpotifyController
        import spotipy

        uri = call.data.get(CONF_SPOTIFY_URI)
        device_name = call.data.get(CONF_DEVICE_NAME)
        _LOGGER.info('HHHHHHHEEEEEEERRRRRREEEEEE')
        _LOGGER.info('Starting spotify on %s (%s)', device_name, slugify(device_name))
        _LOGGER.info('Is something playing on any of these: %s', hass.data[DOMAIN]['chromecasts'])

        transfer_playback = False

        """ 
        PR: add transfer discuss
        The below could possiblty be replaced with
        spotipy.current_playback()['device] and look for name (which is the CC friendly name) and `type` 
        which  is "CastAudio" at least for audio only devies.
        This would require the logic to be moved below `client = spotipy.Spotify(auth=access_token)` 
        """
        for cd in hass.data[DOMAIN]['chromecasts']:
            entity_id = 'media_player.' + slugify(cd['name'])
            entity = hass.states.get(entity_id)
            _LOGGER.debug('entity (%s): %s', entity_id, entity.state)
            if entity is None:
                _LOGGER.error('Could not get entity for chromecast device with name %s (%s)', cd['name'], entity_id)
                continue
            if entity.state == STATE_PLAYING and entity.attributes.get('app_name') == 'Spotify':
                _LOGGER.debug('Found playing chromcast device (%s), will transfer playback.', cd['name'])
                transfer_playback = True
                break

        # Find chromecast device
        # PR: Should use the list already in shared mem from the sensor to cut the scan time for pychromecast (2-3 secs)
        cast = get_chromcase_device(device_name)
        cast.wait()

        account = call.data.get(CONF_SPOTIFY_ACCOUNT)
        user = username
        pwd = password
        if account is not None:
            _LOGGER.debug('setting up with different account than default %s', account)
            user = accounts.get(account).get(CONF_USERNAME)
            pwd = accounts.get(account).get(CONF_PASSWORD)

        # login as real browser to get powerful token
        access_token, expires = get_spotify_token(username=user, password=pwd)

        client = spotipy.Spotify(auth=access_token)

        # launch the app on chromecast
        sp = SpotifyController(access_token, expires)
        cast.register_handler(sp)
        sp.launch_app()

        if not sp.is_launched and not sp.credential_error:
            raise HomeAssistantError('Failed to launch spotify controller due to timeout')
        if not sp.is_launched and sp.credential_error:
            raise HomeAssistantError('Failed to launch spotify controller due to credentials error')

        spotify_device_id = None
        devices_available = client.devices()
        for device in devices_available['devices']:
            if device['id'] == sp.device:
                spotify_device_id = device['id']
                break

        if not spotify_device_id:
            _LOGGER.error('No device with id "{}" known by Spotify'.format(sp.device))
            _LOGGER.error('Known devices: {}'.format(devices_available['devices']))
            return

        if transfer_playback == True:
            transfer_pb(client, spotify_device_id)
        else:
            play(client, spotify_device_id, uri)

    hass.services.register(DOMAIN, 'start', start_casting,
                           schema=SERVICE_START_COMMAND_SCHEMA)

    return True