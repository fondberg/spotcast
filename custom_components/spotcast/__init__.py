import logging
import random
import time
from datetime import datetime

import spotipy
from homeassistant.components import websocket_api
from homeassistant.const import CONF_ENTITY_ID, CONF_OFFSET, CONF_REPEAT
from homeassistant.core import callback

from .const import (
    CONF_ACCOUNTS,
    CONF_DEVICE_NAME,
    CONF_FORCE_PLAYBACK,
    CONF_IGNORE_FULLY_PLAYED,
    CONF_RANDOM,
    CONF_SHUFFLE,
    CONF_SP_DC,
    CONF_SP_KEY,
    CONF_SPOTIFY_ACCOUNT,
    CONF_SPOTIFY_DEVICE_ID,
    CONF_SPOTIFY_URI,
    CONF_START_VOL,
    DOMAIN,
    SCHEMA_PLAYLISTS,
    SCHEMA_WS_ACCOUNTS,
    SCHEMA_WS_CASTDEVICES,
    SCHEMA_WS_DEVICES,
    SCHEMA_WS_PLAYER,
    SERVICE_START_COMMAND_SCHEMA,
    SPOTCAST_CONFIG_SCHEMA,
    WS_TYPE_SPOTCAST_ACCOUNTS,
    WS_TYPE_SPOTCAST_CASTDEVICES,
    WS_TYPE_SPOTCAST_DEVICES,
    WS_TYPE_SPOTCAST_PLAYER,
    WS_TYPE_SPOTCAST_PLAYLISTS,
)
from .helpers import async_wrap, get_cast_devices, get_spotify_devices
from .spotcast_controller import SpotifyCastDevice, SpotifyToken

CONFIG_SCHEMA = SPOTCAST_CONFIG_SCHEMA

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup the Spotcast service."""
    conf = config[DOMAIN]

    sp_dc = conf[CONF_SP_DC]
    sp_key = conf[CONF_SP_KEY]
    accounts = conf.get(CONF_ACCOUNTS)
    spotifyTokenInstances = {}

    def get_token_instance(account=None):
        """Get token instance for account"""
        if account is None or account == "default":
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
        @async_wrap
        def get_playlist():
            """Handle to get playlist"""
            playlistType = msg.get("playlist_type")
            countryCode = msg.get("country_code")
            locale = msg.get("locale", "en")
            limit = msg.get("limit", 10)
            account = msg.get("account", None)

            _LOGGER.debug("websocket_handle_playlists msg: %s", msg)

            client = spotipy.Spotify(auth=get_token_instance(account).access_token)
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
                    locale=locale,
                    country=countryCode,
                    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                    limit=limit,
                    offset=0,
                )
                resp = resp.get("playlists")
            else:
                resp = client.current_user_playlists(limit=limit)

            connection.send_message(websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_playlist())

    @callback
    def websocket_handle_devices(hass, connection, msg):
        @async_wrap
        def get_devices():
            """Handle to get devices. Only for default account"""
            account = msg.get("account", None)
            client = spotipy.Spotify(auth=get_token_instance(account).access_token)
            me_resp = client._get("me")
            resp = get_spotify_devices(hass, me_resp["id"])
            connection.send_message(websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_devices())

    @callback
    def websocket_handle_player(hass, connection, msg):
        @async_wrap
        def get_player():
            """Handle to get player"""
            account = msg.get("account", None)
            _LOGGER.debug("websocket_handle_player msg: %s", msg)
            client = spotipy.Spotify(auth=get_token_instance(account).access_token)
            resp = client._get("me/player")
            connection.send_message(websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_player())

    @callback
    def websocket_handle_accounts(hass, connection, msg):
        """Handle to get accounts"""
        _LOGGER.debug("websocket_handle_accounts msg: %s", msg)
        resp = list(accounts.keys()) if accounts is not None else []
        resp.append("default")
        connection.send_message(websocket_api.result_message(msg["id"], resp))

    @callback
    def websocket_handle_castdevices(hass, connection, msg):
        """Handle to get cast devices for debug purposes"""
        _LOGGER.debug("websocket_handle_castdevices msg: %s", msg)

        known_devices = get_cast_devices(hass)
        _LOGGER.debug("%s", known_devices)
        resp = [
            {
                "uuid": cast_info.uuid,
                "model_name": cast_info.model_name,
                "friendly_name": cast_info.friendly_name,
            }
            for cast_info in known_devices
        ]

        connection.send_message(websocket_api.result_message(msg["id"], resp))

    def play(
        client,
        spotify_device_id,
        uri,
        random_song,
        repeat,
        shuffle,
        position,
        ignore_fully_played,
    ):
        _LOGGER.debug(
            "Playing URI: %s on device-id: %s",
            uri,
            spotify_device_id,
        )
        if uri.find("show") > 0:
            show_episodes_info = client.show_episodes(uri)
            if show_episodes_info and len(show_episodes_info["items"]) > 0:
                if ignore_fully_played:
                    for episode in show_episodes_info["items"]:
                        if not episode["resume_point"]["fully_played"]:
                            episode_uri = episode["external_urls"]["spotify"]
                            break
                else:
                    episode_uri = show_episodes_info["items"][0]["external_urls"][
                        "spotify"
                    ]
                _LOGGER.debug(
                    "Playing episode using uris (latest podcast playlist)= for uri: %s",
                    episode_uri,
                )
                client.start_playback(device_id=spotify_device_id, uris=[episode_uri])
        elif uri.find("episode") > 0:
            _LOGGER.debug("Playing episode using uris= for uri: %s", uri)
            client.start_playback(device_id=spotify_device_id, uris=[uri])

        elif uri.find("track") > 0:
            _LOGGER.debug("Playing track using uris= for uri: %s", uri)
            client.start_playback(device_id=spotify_device_id, uris=[uri])
        else:
            if uri == "random":
                _LOGGER.debug(
                    "Cool, you found the easter egg with playing a random playlist"
                )
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

    def getSpotifyConnectDeviceId(client, device_name):
        devices_available = get_spotify_devices(hass, client._get("me")["id"])
        for device in devices_available["devices"]:
            if device["name"] == device_name:
                return device["id"]
        return None

    def start_casting(call):
        """service called."""
        uri = call.data.get(CONF_SPOTIFY_URI)
        random_song = call.data.get(CONF_RANDOM, False)
        repeat = call.data.get(CONF_REPEAT)
        shuffle = call.data.get(CONF_SHUFFLE)
        start_volume = call.data.get(CONF_START_VOL)
        spotify_device_id = call.data.get(CONF_SPOTIFY_DEVICE_ID)
        position = call.data.get(CONF_OFFSET)
        force_playback = call.data.get(CONF_FORCE_PLAYBACK)
        account = call.data.get(CONF_SPOTIFY_ACCOUNT)
        ignore_fully_played = call.data.get(CONF_IGNORE_FULLY_PLAYED)
        device_name = call.data.get(CONF_DEVICE_NAME)
        entity_id = call.data.get(CONF_ENTITY_ID)

        # login as real browser to get powerful token
        access_token, expires = get_token_instance(account).get_spotify_token()

        # get the spotify web api client
        client = spotipy.Spotify(auth=access_token)
        # first, rely on spotify id given in config
        if not spotify_device_id:
            # if not present, check if there's a spotify connect device with that name
            spotify_device_id = getSpotifyConnectDeviceId(
                client, call.data.get(CONF_DEVICE_NAME)
            )
        if not spotify_device_id:
            # if still no id available, check cast devices and launch the app on chromecast
            spotify_cast_device = SpotifyCastDevice(
                hass,
                call.data.get(CONF_DEVICE_NAME),
                call.data.get(CONF_ENTITY_ID),
            )
            me_resp = client._get("me")
            spotify_cast_device.startSpotifyController(access_token, expires)
            spotify_device_id = spotify_cast_device.getSpotifyDeviceId(
                get_spotify_devices(hass, me_resp["id"])
            )

        if uri is None or uri.strip() == "":
            _LOGGER.debug("Transfering playback")
            current_playback = client.current_playback()
            if current_playback is not None:
                _LOGGER.debug("Current_playback from spotify: %s", current_playback)
                force_playback = True
            _LOGGER.debug("Force playback: %s", force_playback)
            client.transfer_playback(
                device_id=spotify_device_id, force_play=force_playback
            )
        else:
            play(
                client,
                spotify_device_id,
                uri,
                random_song,
                repeat,
                shuffle,
                position,
                ignore_fully_played,
            )
        if shuffle or repeat or start_volume <= 100:
            if start_volume <= 100:
                _LOGGER.debug("Setting volume to %d", start_volume)
                time.sleep(2)
                client.volume(volume_percent=start_volume, device_id=spotify_device_id)
            if shuffle:
                _LOGGER.debug("Turning shuffle on")
                time.sleep(3)
                client.shuffle(state=shuffle, device_id=spotify_device_id)
            if repeat:
                _LOGGER.debug("Turning repeat on")
                time.sleep(3)
                client.repeat(state=repeat, device_id=spotify_device_id)

    # Register websocket and service
    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_PLAYLISTS, websocket_handle_playlists, SCHEMA_PLAYLISTS
    )
    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_DEVICES, websocket_handle_devices, SCHEMA_WS_DEVICES
    )
    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_PLAYER, websocket_handle_player, SCHEMA_WS_PLAYER
    )

    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_ACCOUNTS, websocket_handle_accounts, SCHEMA_WS_ACCOUNTS
    )

    hass.components.websocket_api.async_register_command(
        WS_TYPE_SPOTCAST_CASTDEVICES,
        websocket_handle_castdevices,
        SCHEMA_WS_CASTDEVICES,
    )

    hass.services.register(
        DOMAIN, "start", start_casting, schema=SERVICE_START_COMMAND_SCHEMA
    )

    return True
