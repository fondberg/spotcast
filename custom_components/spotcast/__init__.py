import logging
import voluptuous as vol
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_PASSWORD, CONF_USERNAME)
from homeassistant.components.cast.media_player import KNOWN_CHROMECAST_INFO_KEY
import random
import time

_VERSION = '2.0.0'
DOMAIN = 'spotcast'

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_NAME = 'device_name'
CONF_ENTITY_ID = 'entity_id'
CONF_SPOTIFY_URI = 'uri'
CONF_ACCOUNTS = 'accounts'
CONF_SPOTIFY_ACCOUNT = 'account'
CONF_TRANSFER_PLAYBACK = 'transfer_playback'
CONF_RANDOM = 'random_song'

SERVICE_START_COMMAND_SCHEMA = vol.Schema({
    vol.Optional(CONF_DEVICE_NAME): cv.string,
    vol.Optional(CONF_ENTITY_ID): cv.string,
    vol.Optional(CONF_SPOTIFY_URI): cv.string,
    vol.Optional(CONF_SPOTIFY_ACCOUNT): cv.string,
    vol.Optional(CONF_TRANSFER_PLAYBACK): cv.boolean,
    vol.Optional(CONF_RANDOM): cv.boolean
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

    # sensor
    # hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    # service
    def get_chromcast_device(device_name):
        import pychromecast

        # Get cast from discovered devices of cast platform
        known_devices = hass.data.get(KNOWN_CHROMECAST_INFO_KEY, [])
        cast_info = next((x for x in known_devices if x.friendly_name == device_name), None)
        _LOGGER.debug('cast info: %s', cast_info)
        if cast_info:
            return pychromecast._get_chromecast_from_host((
                cast_info.host, cast_info.port, cast_info.uuid,
                cast_info.model_name, cast_info.friendly_name
            ))
        _LOGGER.error('Could not find device %s from hass.data, falling back to pychromecast scan', device_name)

        # Discover devices manually
        chromecasts = pychromecast.get_chromecasts()
        cast = None
        for _cast in chromecasts:
            if _cast.name == device_name:
                _LOGGER.debug('Found cast device: %s', cast)
                return _cast

        raise HomeAssistantError('Could not find device with name {}'.format(device_name))


    def get_spotify_token(username, password):
        import spotify_token as st
        data = st.start_session(username, password)
        access_token = data[0]
        expires = data[1] - int(time.time())
        return access_token, expires

    def play(client, spotify_device_id, uri, random_song):
        # import spotipy
        # import http.client as http_client
        # spotipy.trace = True
        # spotipy.trace_out = True
        # http_client.HTTPConnection.debuglevel = 1

        _LOGGER.debug('Version: %s, playing URI: %s on device-id: %s', _VERSION, uri, spotify_device_id)
        if uri.find('track') > 0:
            _LOGGER.debug('Playing track using uris= for uri: %s', uri)
            client.start_playback(device_id=spotify_device_id, uris=[uri])
        else:
            if uri == 'random':
                _LOGGER.debug('Cool, you found the easter egg with playing a random playlist')
                playlists = client.user_playlists('me', 50)
                no_playlists = len(playlists['items'])
                uri = playlists['items'][random.randint(0, no_playlists - 1)]['uri']
            kwargs = {'device_id': spotify_device_id, 'context_uri': uri}
            if random_song:
                results = client.user_playlist_tracks("me", uri)
                position = random.randint(0, results['total'] - 1)
                _LOGGER.debug('Start playback at random position: %s', position)
                kwargs['offset'] = {'position': position}

            _LOGGER.debug('Playing context uri using context_uri for uri: "%s" (random_song: %s)', uri, random_song)
            client.start_playback(**kwargs)

    def transfer_pb(client, spotify_device_id):
        _LOGGER.debug('Transfering playback')
        client.transfer_playback(device_id=spotify_device_id, force_play=True)

    def start_casting(call):
        """service called."""

        from pychromecast.controllers.spotify import SpotifyController
        import spotipy
        transfer_playback = False

        uri = call.data.get(CONF_SPOTIFY_URI)
        random_song = call.data.get(CONF_RANDOM, False)

        # Get device name from tiehr device_name or entity_id
        device_name = None
        if call.data.get(CONF_DEVICE_NAME) is None:
            entity_id = call.data.get(CONF_ENTITY_ID)
            if entity_id is None:
                raise HomeAssistantError('Either entity_id or device_name must be specified')
            entity_states = hass.states.get(entity_id)
            if entity_states is None:
                _LOGGER.error('Could not find entity_id: %s', entity_id)
            else:
                device_name = entity_states.attributes.get('friendly_name')
        else:
            device_name = call.data.get(CONF_DEVICE_NAME)

        if device_name is None or device_name.strip() == '':
            raise HomeAssistantError('device_name is empty')

        # Find chromecast device
        cast = get_chromcast_device(device_name)
        _LOGGER.debug('Found cast device: %s', cast)
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

        # get the spotify web api client
        client = spotipy.Spotify(auth=access_token)

        # Check if something is playing

        if uri is None or uri.strip() == '' or call.data.get(CONF_TRANSFER_PLAYBACK):
            current_playback = client.current_playback()
            if current_playback is not None:
                _LOGGER.debug('current_playback from spotipy: %s', current_playback)
                transfer_playback = True

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
            play(client, spotify_device_id, uri, random_song)

    hass.services.register(DOMAIN, 'start', start_casting,
                           schema=SERVICE_START_COMMAND_SCHEMA)

    return True
