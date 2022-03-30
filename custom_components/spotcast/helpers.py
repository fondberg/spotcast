from __future__ import annotations

import asyncio
import logging
import requests
import urllib
import difflib
import random
from functools import partial, wraps

from homeassistant.components.cast.media_player import CastDevice
from homeassistant.components.spotify.media_player import SpotifyMediaPlayer
from homeassistant.helpers import entity_platform

# import for type inference
import spotipy

_LOGGER = logging.getLogger(__name__)


def get_spotify_devices(hass, spotify_user_id):
    platforms = entity_platform.async_get_platforms(hass, "spotify")
    spotify_media_player = None
    for platform in platforms:
        if platform.domain != "media_player":
            continue

        for entity in platform.entities.values():
            if (
                isinstance(entity, SpotifyMediaPlayer)
                and entity.unique_id == spotify_user_id
            ):

                try:
                    entity_devices = entity._devices
                except(AttributeError):
                    entity_devices = entity.data.devices.data

                _LOGGER.debug(f"get_spotify_devices: {entity.entity_id}: {entity.name}: %s", entity_devices)
                spotify_media_player = entity
                break

    if spotify_media_player:
        # Need to come from media_player spotify's sp client due to token issues
        try:
            resp = spotify_media_player._spotify.devices()
        except(AttributeError):
            resp = spotify_media_player.data.client.devices()

        _LOGGER.debug("get_spotify_devices: %s", resp)
        
        return resp

def get_spotify_install_status(hass):

    platform_string = "spotify"
    platforms = entity_platform.async_get_platforms(hass, platform_string)
    platform_count = len(platforms)

    if platform_count == 0:
        _LOGGER.error("%s integration not found", platform_string)
    else:
        _LOGGER.debug("%s integration found", platform_string)

    return platform_count != 0


def get_cast_devices(hass):
    platforms = entity_platform.async_get_platforms(hass, "cast")
    cast_infos = []
    for platform in platforms:
        if platform.domain != "media_player":
            continue
        for entity in platform.entities.values():
            if isinstance(entity, CastDevice):
                _LOGGER.debug(
                    f"get_cast_devices: {entity.entity_id}: {entity.name} cast info: %s",
                    entity._cast_info,
                )
                cast_infos.append(entity._cast_info)
    return cast_infos


# Async wrap sync function
def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run

def get_search_results(search:str, spotify_client:spotipy.Spotify, country:str=None) -> str:

    _LOGGER.debug("using search query to find uri")

    SEARCH_TYPES = ["artist", "album", "track", "playlist"]

    search = search.upper()

    results = []

    for searchType in SEARCH_TYPES:

        try:

            result = spotify_client.search(
                searchType + ":" + search,
                limit=1,
                offset=0,
                type=searchType,
                market=country)[searchType + 's']['items'][0]

            results.append(
                {
                    'name': result['name'].upper(),
                    'uri': result['uri']
                }
            )

            _LOGGER.debug("search result for %s: %s", searchType, result['name'])

        except IndexError:
            pass

    bestMatch = sorted(results, key=lambda x: difflib.SequenceMatcher(None, x['name'], search).ratio(), reverse=True)[0]

    _LOGGER.debug("Best match for %s is %s", search, bestMatch['name'])

    return bestMatch['uri']

def get_random_playlist_from_category(spotify_client:spotipy.Spotify, category:str, country:str=None, limit:int=20) -> str:
    
    if country is None:
        
        _LOGGER.debug(f"Get random playlist among {limit} playlists from category {category}, no country specified.")

    else:

        _LOGGER.debug(f"Get random playlist among {limit} playlists from category {category} in country {country}")

        # validate category and country are valid entries
        if country.upper() not in spotify_client.country_codes:
            _LOGGER.error(f"{country} is not a valid country code")
            return None
    
    # get list of playlist from category and localisation provided
    try:
        playlists = spotify_client.category_playlists(category_id=category, country=country, limit=limit)["playlists"]["items"]
    except spotipy.exceptions.SpotifyException as e:
        _LOGGER.error(e.msg)
        return None

    # choose one at random
    chosen = random.choice(playlists)

    _LOGGER.debug(f"Chose playlist {chosen['name']} ({chosen['uri']}) from category {category}.")

    return chosen['uri']

def is_valid_uri(uri: str) -> bool:
    
    # list of possible types
    types = [
        "artist",
        "album",
        "track",
        "playlist",
        "show",
        "episode"
    ]

    # split the string
    elems = uri.split(":")

    # validate number of sub elements
    if len(elems) != 3:
        _LOGGER.error(f"[{uri}] is not a valid URI. The format should be [spotify:<type>:<unique_id>]")
        return False

    # check correct format of the sub elements
    if elems[0].lower() != "spotify":
        _LOGGER.error(f"This is not a valid Spotify URI. This should start with [spotify], but instead starts with [{elems[0]}]")
        return False

    if elems[1].lower() not in types:
        _LOGGER.error(f"{elems[1]} is not a valid type for Spotify request. Please make sure to use the following list {str(types)}")
        return False

    if "?" in elems[2]:
        _LOGGER.warning(f"{elems[2]} contains query character. This should work, but you should probably remove it and anything after.")
    
    # return True if all test passes
    return True

def is_empty_str(string:str) -> bool:
    return string is None or string.strip() == ""
