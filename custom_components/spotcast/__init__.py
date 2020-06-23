import logging
import voluptuous as vol
from homeassistant.components import http, websocket_api
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.components.cast.media_player import KNOWN_CHROMECAST_INFO_KEY
import random
import time

_VERSION = "3.2.1"
DOMAIN = "spotcast"

_LOGGER = logging.getLogger(__name__)

CONF_SPOTIFY_DEVICE_ID = "spotify_device_id"
CONF_DEVICE_NAME = "device_name"
CONF_ENTITY_ID = "entity_id"
CONF_SPOTIFY_URI = "uri"
CONF_ACCOUNTS = "accounts"
CONF_SPOTIFY_ACCOUNT = "account"
CONF_FORCE_PLAYBACK = "force_playback"
CONF_RANDOM = "random_song"
CONF_REPEAT = "repeat"
CONF_SHUFFLE = "shuffle"
CONF_OFFSET = "offset"
CONF_SP_DC = "sp_dc"
CONF_SP_KEY = "sp_key"

WS_TYPE_SPOTCAST_PLAYLISTS = "spotcast/playlists"

SCHEMA_PLAYLISTS = websocket_api.BASE_COMMAND_MESSAGE_SCHEMA.extend(
    {
        vol.Required("type"): WS_TYPE_SPOTCAST_PLAYLISTS,
        vol.Required("playlist_type"): str,
        vol.Optional("limit"): int,
        vol.Optional("country_code"): str,
        vol.Optional("locale"): str,
    }
)

SERVICE_START_COMMAND_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_DEVICE_NAME): cv.string,
        vol.Optional(CONF_SPOTIFY_DEVICE_ID): cv.string,
        vol.Optional(CONF_ENTITY_ID): cv.string,
        vol.Optional(CONF_SPOTIFY_URI): cv.string,
        vol.Optional(CONF_SPOTIFY_ACCOUNT): cv.string,
        vol.Optional(CONF_FORCE_PLAYBACK, default=False): cv.boolean,
        vol.Optional(CONF_RANDOM, default=False): cv.boolean,
        vol.Optional(CONF_REPEAT, default="off"): cv.string,
        vol.Optional(CONF_SHUFFLE, default=False): cv.boolean,
        vol.Optional(CONF_OFFSET, default=0): cv.string,
    }
)

ACCOUNTS_SCHEMA = vol.Schema(
    {vol.Required(CONF_SP_DC): cv.string, vol.Required(CONF_SP_KEY): cv.string,}
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_SP_DC): cv.string,
                vol.Required(CONF_SP_KEY): cv.string,
                vol.Optional(CONF_ACCOUNTS): cv.schema_with_slug_keys(ACCOUNTS_SCHEMA),
            }
        ),
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Setup the Spotcast service."""
    conf = config[DOMAIN]

    sp_dc = conf[CONF_SP_DC]
    sp_key = conf[CONF_SP_KEY]
    accounts = conf.get(CONF_ACCOUNTS)
    spotifyTokenInstances = {}

    def get_token_instance(account = None):
        """ Get token instance for account """
        if account is None:
            account = "default"
            dc = sp_dc
            key = sp_key
        else:
            dc = accounts.get(account).get(CONF_SP_DC)
            key = accounts.get(account).get(CONF_SP_KEY)

        _LOGGER.debug("setting up with  account %s", account)
        if account not in spotifyTokenInstances:
            spotifyTokenInstances[account] = SpotifyToken(dc, key)
        return spotifyTokenInstances[account]

    @callback
    def websocket_handle_playlists(hass, connection, msg):
        """Handle to get playlist"""
        import spotipy

        playlistType = msg.get("playlist_type")
        countryCode = msg.get("country_code")
        locale = msg.get("locale", "en")
        limit = msg.get("limit", 10)

        _LOGGER.debug("websocket msg: %s", msg)

        client = spotipy.Spotify(auth=get_token_instance().access_token)
        resp = {}

        if playlistType == "discover-weekly":
            resp = client._get(
                "views/made-for-x",
                content_limit=limit,
                locale=locale,
                platform="web",
                types="album,playlist,artist,show,station",
                limit=limit,
                offset=0,
            )
            resp = resp.get("content")
        elif playlistType == "featured":
            resp = client.featured_playlists(
                locale=locale, country=countryCode, timestamp=None, limit=limit, offset=0
            )
            resp = resp.get("playlists")
        else:
            resp = client.user_playlists("me", limit)

        connection.send_message(websocket_api.result_message(msg["id"], resp))

    def play(client, spotify_device_id, uri, random_song, repeat, shuffle, position):
        _LOGGER.debug(
            "Version: %s, playing URI: %s on device-id: %s", _VERSION, uri, spotify_device_id
        )
        if uri.find("track") > 0:
            _LOGGER.debug("Playing track using uris= for uri: %s", uri)
            client.start_playback(device_id=spotify_device_id, uris=[uri])
        else:
            if uri == "random":
                _LOGGER.debug("Cool, you found the easter egg with playing a random playlist")
                playlists = client.user_playlists("me", 50)
                no_playlists = len(playlists["items"])
                uri = playlists["items"][random.randint(0, no_playlists - 1)]["uri"]
            kwargs = {"device_id": spotify_device_id, "context_uri": uri}

            if random_song:
                if uri.find("album") > 0:
                    results = client.album_tracks(uri)
                    position = random.randint(0, results["total"] - 1)
                elif uri.find("playlist") > 0:
                    results = client.playlist_tracks(uri)
                    position = random.randint(0, results["total"] - 1)
                _LOGGER.debug("Start playback at random position: %s", position)
            if uri.find("artist") < 1:
                kwargs["offset"] = {"position": position}
            _LOGGER.debug(
                'Playing context uri using context_uri for uri: "%s" (random_song: %s)',
                uri,
                random_song,
            )
            client.start_playback(**kwargs)
        if shuffle or repeat:
            time.sleep(3)
            if shuffle:
                _LOGGER.debug("Turning shuffle on")
                time.sleep(2)
                client.shuffle(state=shuffle, device_id=spotify_device_id)
            if repeat:
                _LOGGER.debug("Turning repeat on")
                time.sleep(2)
                client.repeat(state=repeat, device_id=spotify_device_id)


    def getSpotifyConnectDeviceId(client, device_name):
        devices_available = client.devices()
        for device in devices_available["devices"]:
            if device["name"] == device_name:
                return device["id"]
        return None

    def start_casting(call):
        """service called."""
        import spotipy

        uri = call.data.get(CONF_SPOTIFY_URI)
        random_song = call.data.get(CONF_RANDOM, False)
        repeat = call.data.get(CONF_REPEAT)
        shuffle = call.data.get(CONF_SHUFFLE)
        spotify_device_id = call.data.get(CONF_SPOTIFY_DEVICE_ID)
        position = call.data.get(CONF_OFFSET)
        force_playback = call.data.get(CONF_FORCE_PLAYBACK)
        account = call.data.get(CONF_SPOTIFY_ACCOUNT)

        # login as real browser to get powerful token
        access_token, expires = get_token_instance(account).get_spotify_token()

        # get the spotify web api client
        client = spotipy.Spotify(auth=access_token)

        # first, rely on spotify id given in config
        if not spotify_device_id:
            # if not present, check if there's a spotify connect device with that name
            spotify_device_id = getSpotifyConnectDeviceId(client, call.data.get(CONF_DEVICE_NAME))
        if not spotify_device_id:
            # if still no id available, check cast devices and launch the app on chromecast
            spotify_cast_device = SpotifyCastDevice(
                hass, call.data.get(CONF_DEVICE_NAME), call.data.get(CONF_ENTITY_ID)
            )
            spotify_cast_device.startSpotifyController(access_token, expires)
            spotify_device_id = spotify_cast_device.getSpotifyDeviceId(client)

        if uri is None or uri.strip() == "":
            _LOGGER.debug("Transfering playback")
            current_playback = client.current_playback()
            if current_playback is not None:
                _LOGGER.debug("Current_playback from spotipy: %s", current_playback)
                force_playback = True
            _LOGGER.debug("Force playback: %s", force_playback)
            client.transfer_playback(device_id=spotify_device_id, force_play=force_playback)
        else:
            play(client, spotify_device_id, uri, random_song, repeat, shuffle, position)

    # Register websocket and service
    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_PLAYLISTS, websocket_handle_playlists, SCHEMA_PLAYLISTS
    )

    hass.services.register(DOMAIN, "start", start_casting, schema=SERVICE_START_COMMAND_SCHEMA)

    return True


class SpotifyToken:
    """Represents a spotify token."""

    sp_dc = None
    sp_key = None
    _access_token = None
    _token_expires = 0

    def __init__(self, sp_dc, sp_key):
        self.sp_dc = sp_dc
        self.sp_key = sp_key

    def ensure_token_valid(self):
        if float(self._token_expires) > time.time():
            return True
        self.get_spotify_token()

    @property
    def access_token(self):
        self.ensure_token_valid()
        _LOGGER.debug("expires: %s time: %s", self._token_expires, time.time())
        return self._access_token

    def get_spotify_token(self):
        import spotify_token as st
        self._access_token, self._token_expires = st.start_session(self.sp_dc, self.sp_key)
        expires = self._token_expires - int(time.time())
        return self._access_token, expires


class SpotifyCastDevice:
    """Represents a spotify device."""

    hass = None
    castDevice = None
    spotifyController = None

    def __init__(self, hass, call_device_name, call_entity_id):
        """Initialize a spotify cast device."""
        self.hass = hass

        # Get device name from either device_name or entity_id
        device_name = None
        if call_device_name is None:
            entity_id = call_entity_id
            if entity_id is None:
                raise HomeAssistantError("Either entity_id or device_name must be specified")
            entity_states = hass.states.get(entity_id)
            if entity_states is None:
                _LOGGER.error("Could not find entity_id: %s", entity_id)
            else:
                device_name = entity_states.attributes.get("friendly_name")
        else:
            device_name = call_device_name

        if device_name is None or device_name.strip() == "":
            raise HomeAssistantError("device_name is empty")

        # Find chromecast device
        self.castDevice = self.getChromecastDevice(device_name)
        _LOGGER.debug("Found cast device: %s", self.castDevice)
        self.castDevice.wait()

    def getChromecastDevice(self, device_name):
        import pychromecast

        # Get cast from discovered devices of cast platform
        known_devices = self.hass.data.get(KNOWN_CHROMECAST_INFO_KEY, [])
        cast_info = next((x for x in known_devices if x.friendly_name == device_name), None)
        _LOGGER.debug("cast info: %s", cast_info)

        if cast_info:
            return pychromecast._get_chromecast_from_host(
                (
                    cast_info.host,
                    cast_info.port,
                    cast_info.uuid,
                    cast_info.model_name,
                    cast_info.friendly_name,
                )
            )
        _LOGGER.error(
            "Could not find device %s from hass.data, falling back to pychromecast scan",
            device_name,
        )

        # Discover devices manually
        chromecasts = pychromecast.get_chromecasts()
        for _cast in chromecasts:
            if _cast.name == device_name:
                _LOGGER.debug("Fallback, found cast device: %s", _cast)
                return _cast

        raise HomeAssistantError("Could not find device with name {}".format(device_name))

    def startSpotifyController(self, access_token, expires):
        from pychromecast.controllers.spotify import SpotifyController

        sp = SpotifyController(access_token, expires)
        self.castDevice.register_handler(sp)
        sp.launch_app()

        if not sp.is_launched and not sp.credential_error:
            raise HomeAssistantError("Failed to launch spotify controller due to timeout")
        if not sp.is_launched and sp.credential_error:
            raise HomeAssistantError("Failed to launch spotify controller due to credentials error")

        self.spotifyController = sp

    def getSpotifyDeviceId(self, client):
        # Look for device
        spotify_device_id = None
        devices_available = client.devices()
        for device in devices_available["devices"]:
            if device["id"] == self.spotifyController.device:
                spotify_device_id = device["id"]
                break

        if not spotify_device_id:
            _LOGGER.error(
                'No device with id "{}" known by Spotify'.format(self.spotifyController.device)
            )
            _LOGGER.error("Known devices: {}".format(devices_available["devices"]))
            raise HomeAssistantError("Failed to get device id from Spotify")
        return spotify_device_id
