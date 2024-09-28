from __future__ import annotations

import collections
import json
import logging
import random
import time
from asyncio import run_coroutine_threadsafe
from collections import OrderedDict
from datetime import datetime

import aiohttp
import pychromecast
import spotipy
from homeassistant.components.cast.helpers import ChromeCastZeroconf
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from requests import TooManyRedirects
from .error import TokenError
from .const import CONF_SP_DC, CONF_SP_KEY
from .helpers import get_cast_devices, get_spotify_devices, get_spotify_media_player
from .spotify_controller import SpotifyController

_LOGGER = logging.getLogger(__name__)


class SpotifyCastDevice:
    """Represents a spotify device."""

    spotify_controller: SpotifyController | None = None

    def __init__(
        self, hass: HomeAssistant, device_name: str | None, entity_id: str | None
    ) -> None:
        """Initialize a spotify cast device."""
        self.hass = hass

        # Get device name from entity_id
        if device_name is None:
            if entity_id is None:
                raise HomeAssistantError(
                    "Either entity_id or device_name must be specified"
                )
            entity_states = hass.states.get(entity_id)
            if entity_states is None:
                _LOGGER.error("Could not find entity_id: %s", entity_id)
            else:
                device_name = entity_states.attributes.get("friendly_name")

        if device_name is None or device_name.strip() == "":
            raise HomeAssistantError("device_name is empty")

        self.device_name = device_name

    def get_chromecast_device(self) -> pychromecast.Chromecast:
        # Get cast from discovered devices of cast platform
        known_devices = get_cast_devices(self.hass)

        _LOGGER.debug("Chromecast devices: %s", known_devices)
        cast_info = next(
            (
                castinfo
                for castinfo in known_devices
                if castinfo.friendly_name == self.device_name
            ),
            None,
        )
        _LOGGER.debug("Cast info: %s", cast_info)
        if cast_info:
            return pychromecast.get_chromecast_from_cast_info(
                cast_info.cast_info, ChromeCastZeroconf.get_zeroconf()
            )
        _LOGGER.error(
            "Could not find Chromecast device %s from hass.data",
            self.device_name,
        )
        raise HomeAssistantError(
            "Could not find Chromecast device with name {}".format(self.device_name)
        )

    def start_spotify_controller(self, access_token: str, expires: int) -> None:
        cast_device = self.get_chromecast_device()
        _LOGGER.debug("Found cast device: %s", cast_device)
        cast_device.wait()

        sp = SpotifyController(cast_device, access_token, expires)
        cast_device.register_handler(sp)
        sp.launch_app()

        if not sp.is_launched and not sp.credential_error:
            raise HomeAssistantError(
                "Failed to launch spotify controller due to timeout"
            )
        if not sp.is_launched and sp.credential_error:
            raise HomeAssistantError(
                "Failed to launch spotify controller due to credentials error"
            )

        self.spotify_controller = sp

    def get_device_id(self) -> str:
        if self.spotify_controller is None:
            raise HomeAssistantError("SpotifyController is not started")
        return self.spotify_controller.device


class SpotifyToken:
    """Represents a spotify token for an account."""

    hass = None
    sp_dc = None
    sp_key = None
    _access_token = None
    _token_expires = 0

    def __init__(self, hass: HomeAssistant, sp_dc: str, sp_key: str) -> None:
        self.hass = hass
        self.sp_dc = sp_dc
        self.sp_key = sp_key

    def ensure_token_valid(self) -> None:
        if float(self._token_expires) > time.time():
            return
        self.get_spotify_token()

    @property
    def access_token(self) -> str:
        self.ensure_token_valid()
        _LOGGER.debug("expires: %s time: %s", self._token_expires, time.time())
        return self._access_token

    def get_spotify_token(self) -> tuple[str, int]:
        try:
            self._access_token, self._token_expires = run_coroutine_threadsafe(
                self.start_session(), self.hass.loop
            ).result()
            expires = self._token_expires - int(time.time())
            return self._access_token, expires
        except TooManyRedirects:
            _LOGGER.error(
                "Could not get spotify token. sp_dc and sp_key could be "
                "expired. Please update in config."
            )
            raise HomeAssistantError("Expired sp_dc, sp_key")
        except (TokenError, Exception):  # noqa: E722
            raise HomeAssistantError("Could not get spotify token.")

    async def start_session(self) -> tuple[str, int]:
        """ Starts session to get access token. """
        cookies = {"sp_dc": self.sp_dc, "sp_key": self.sp_key}

        async with aiohttp.ClientSession(cookies=cookies) as session:

            headers = {
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
                    "Safari/537.36"
                )
            }

            async with session.get(
                (
                    "https://open.spotify.com/get_access_token?reason="
                    "transport&productType=web_player"
                ),
                allow_redirects=False,
                headers=headers,
            ) as response:
                if (
                    response.status == 302
                    and response.headers["Location"]
                    == "/get_access_token?reason=transport&productType=web_player&_authfailed=1"
                ):
                    _LOGGER.error(
                        "Unsuccessful token request, received code 302 and "
                        "Location header %s. sp_dc and sp_key could be "
                        "expired. Please update in config.",
                        response.headers["Location"],
                    )
                    raise HomeAssistantError("Expired sp_dc, sp_key")
                if response.status != 200:
                    _LOGGER.info(
                        "Unsuccessful token request, received code %i", response.status
                    )
                    raise TokenError()

                data = await response.text()

        config = json.loads(data)
        access_token = config["accessToken"]
        expires_timestamp = config["accessTokenExpirationTimestampMs"]
        expiration_date = int(expires_timestamp) // 1000

        return access_token, expiration_date


class SpotcastController:

    spotifyTokenInstances = {}
    accounts: dict = {}

    def __init__(
        self,
        hass: HomeAssistant,
        sp_dc: str,
        sp_key: str,
        accs: collections.OrderedDict,
    ) -> None:
        if accs:
            self.accounts = accs
        self.accounts["default"] = OrderedDict([("sp_dc", sp_dc), ("sp_key", sp_key)])
        self.hass = hass

    def get_token_instance(self, account: str | None = None) -> SpotifyToken:
        """Get token instance for account"""
        if account is None:
            account = "default"

        # TODO: add error logging when user provide invalid account
        # name
        dc = self.accounts.get(account).get(CONF_SP_DC)
        key = self.accounts.get(account).get(CONF_SP_KEY)

        _LOGGER.debug("Setting up with account %s", account)
        if account not in self.spotifyTokenInstances:
            self.spotifyTokenInstances[account] = SpotifyToken(self.hass, dc, key)
        return self.spotifyTokenInstances[account]

    def get_spotify_client(self, account: str | None) -> spotipy.Spotify:
        return spotipy.Spotify(auth=self.get_token_instance(account).access_token)

    def query_spotify_device_id(
        self,
        user_id: str,
        device_name: str | None,
        spotify_device_ids: list[str],
        max_retries: int = 1,
        error: bool = False,
    ) -> str | None:
        _LOGGER.debug(
            'Searching for a Spotify device with the name "%s" or IDs in %s',
            device_name,
            spotify_device_ids,
        )
        media_player = get_spotify_media_player(self.hass, user_id)
        attempt = 0
        devices = None
        while attempt < max_retries:
            devices_available = get_spotify_devices(media_player)
            if devices := devices_available["devices"]:
                for device in devices:
                    if (
                        device_name is not None
                        and device["name"] == device_name
                        or device["id"] in spotify_device_ids
                    ):
                        _LOGGER.debug("Found matching Spotify device: %s", device)
                        return device["id"]
            sleep_secs = random.uniform(1.5, 1.8) ** attempt
            time.sleep(sleep_secs)
            attempt += 1
        if error:
            _LOGGER.error(
                'No device with the name "%s" or ID "%s" is known to Spotify. Known devices: %s',
                device_name,
                spotify_device_ids,
                devices,
            )
        return None


    def get_spotify_device_id(
        self,
        account: str | None,
        spotify_device_id: str | None,
        device_name: str | None,
        entity_id: str | None,
    ) -> str:
        search_device_ids: list[str] = []
        if spotify_device_id is not None:
            search_device_ids.append(spotify_device_id)
        # login as real browser to get powerful token
        access_token, expires = self.get_token_instance(account).get_spotify_token()
        # get the spotify web api client
        client = spotipy.Spotify(auth=access_token)
        user_id = client._get("me")["id"]
        # first, check if spotify id is already available
        found_spotify_device_id = self.query_spotify_device_id(
            user_id, device_name, search_device_ids
        )
        if found_spotify_device_id is None:
            # if device id is still not available, launch the app on chromecast
            spotify_cast_device = SpotifyCastDevice(
                self.hass,
                device_name,
                entity_id,
            )
            spotify_cast_device.start_spotify_controller(access_token, expires)
            # get spotify device id from SpotifyController
            controller_device_id = spotify_cast_device.get_device_id()
            if controller_device_id not in search_device_ids:
                search_device_ids.append(controller_device_id)
            found_spotify_device_id = self.query_spotify_device_id(
                user_id, device_name, search_device_ids, max_retries=5, error=True
            )
        if found_spotify_device_id is None:
            raise HomeAssistantError("Failed to get device ID from Spotify")
        return found_spotify_device_id


    def play(
        self,
        client: spotipy.Spotify,
        spotify_device_id: str,
        uri: str,
        random_song: bool,
        position: str,
        ignore_fully_played: str,
        country_code: str | None = None,
    ) -> None:
        _LOGGER.debug(
            "Playing URI: %s on device-id: %s",
            uri,
            spotify_device_id,
        )

        if uri.find("show") > 0:
            show_episodes_info = client.show_episodes(uri, market=country_code)
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
                    (
                        "Playing episode using uris (latest podcast playlist)="
                        " for uri: %s"
                    ),
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
                    "Cool, you found the easter egg with playing a random" " playlist"
                )
                playlists = client.user_playlists("me", 50)
                no_playlists = len(playlists["items"])
                uri = playlists["items"][random.randint(0, no_playlists - 1)]["uri"]
            kwargs = {"device_id": spotify_device_id, "context_uri": uri}

            if random_song:
                if uri.find("album") > 0:
                    results = client.album_tracks(uri, market=country_code)
                    position = random.randint(0, int(results["total"]) - 1)
                elif uri.find("playlist") > 0:
                    results = client.playlist_tracks(uri)
                    position = random.randint(0, int(results["total"]) - 1)
                elif uri.find("collection") > 0:
                    results = client.current_user_saved_tracks()
                    position = random.randint(0, int(results["total"]) - 1)
                _LOGGER.debug(
                    "Start playback at random position: %s", position)
            if uri.find("artist") < 1:
                kwargs["offset"] = {"position": position}
            _LOGGER.debug(
                (
                    'Playing context uri using context_uri for uri: "%s" '
                    "(random_song: %s)"
                ),
                uri,
                random_song,
            )
            client.start_playback(**kwargs)

    def get_playlists(
        self,
        account: str,
        playlist_type: str,
        country_code: str,
        locale: str,
        limit: int,
    ) -> dict:
        client = self.get_spotify_client(account)
        resp = {}

        if playlist_type == "discover-weekly":
            playlist_type = "made-for-x"

        if playlist_type == "user" or playlist_type == "default" or playlist_type == "":
            resp = client.current_user_playlists(limit=limit)

        elif playlist_type == "featured":
            resp = client.featured_playlists(
                locale=locale,
                country=country_code,
                timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                limit=limit,
                offset=0,
            )
            resp = resp.get("playlists")
        else:
            resp = client._get(
                "views/" + playlist_type,
                content_limit=limit,
                locale=locale,
                platform="web",
                types="album,playlist,artist,show,station",
                limit=limit,
                offset=0,
            )
            resp = resp.get("content")

        return resp
