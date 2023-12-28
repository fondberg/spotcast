from __future__ import annotations

import asyncio
import logging
import requests
import urllib
import time
import difflib
import random
from functools import partial, wraps

import homeassistant.core as ha_core
from homeassistant.components.cast.media_player import CastDevice
from homeassistant.components.spotify.media_player import SpotifyMediaPlayer
from homeassistant.helpers import entity_platform
from homeassistant.exceptions import HomeAssistantError

# import for type inference
import spotipy

_LOGGER = logging.getLogger(__name__)


def get_spotify_media_player(hass: ha_core.HomeAssistant, spotify_user_id: str) -> SpotifyMediaPlayer:
    """Get the spotify media player entity from hass."""
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
        return spotify_media_player
    else:
        raise HomeAssistantError("Could not find spotify media player.")


def get_spotify_devices(spotify_media_player: SpotifyMediaPlayer):
    if spotify_media_player:
        # Need to come from media_player spotify's sp client due to token issues
        try:
            spotify_devices = spotify_media_player._spotify.devices()
        except(AttributeError):
            spotify_devices = spotify_media_player.data.client.devices()

        _LOGGER.debug("get_spotify_devices: %s", spotify_devices)
        
        return spotify_devices
    return []

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

def get_top_tracks(artistName:str, spotify_client:spotipy.Spotify, limit:int=20, country:str = None):

    _LOGGER.debug("Searching for top tracks for the artist: %s", artistName)
    searchType = "artist"
    search = searchType + ":" + artistName

    artistUri = ""

    # get artist uri
    try:

        artist = spotify_client.search(
            artistName,
            limit=1,
            offset=0,
            type="artist",
            market=country)["artists"]['items'][0]

        _LOGGER.debug("found artist %s: %s", artist['name'], artist['uri'])
        artistUri = artist['uri']

    except IndexError:
        pass

    results = spotify_client.artist_top_tracks(artistUri)
    for track in results['tracks'][:10]:
        _LOGGER.debug('track    : ' + track['name'])

    return results['tracks']

def get_search_string(search:str, artistName:str) -> str:
    finalString = search.upper()
    if not is_empty_str(artistName):
        finalString += " artist:" + artistName
    return finalString

def get_search_results(search:str, spotify_client:spotipy.Spotify, artistName:str=None, limit:int=10, searchType:str=None, country:str=None):
    _LOGGER.debug("using search query to find uri")
    searchResults = []

    if is_empty_str(search) and artistName != None:
        searchResults = get_top_tracks(artistName, spotify_client)
        _LOGGER.debug("Playing top tracks for artist: %s", searchResults[0]['name'])
    else:
        # Get search type
        if searchType == "tracks" and not is_empty_str(artistName):
            search = get_search_string(search, artistName)
        
        resultKey = "playlists" if searchType == "playlist" else "tracks"

        try:
            searchResults = spotify_client.search(
                search,
                limit,
                offset=0,
                type=searchType,
                market=country)[resultKey]['items']
        except IndexError:
            pass
        
        if searchType == "playlist":    
            tempResults = searchResults
            searchResults = []
            for result in tempResults:
                if result["name"].lower() == search.lower() or result["name"].lower() in search.lower():
                    searchResults = [
                        result
                    ]
                    break
        
        if len(searchResults) > 0:
            _LOGGER.debug("Found %d results for %s. First item name: %s", len(searchResults), search, searchResults[0]['name'])

    return searchResults

def search_tracks(search:str, spotify_client:spotipy.Spotify,
                            appendToQueue:bool=False, shuffle:bool=False, startRandom:bool=False,
                            limit:int=20, artistName:str=None, searchType:str=None, country:str=None):
    results = get_search_results(search, spotify_client, artistName, limit, searchType, country)
    if len(results) > 0:
        firstResult = [results[0]]
        if not startRandom:
            results = results[1:limit]
        if shuffle:
            random.shuffle(results)
        if not startRandom:
            results = firstResult + results

    return results

def add_tracks_to_queue(spotify_client:spotipy.Spotify, tracks:list=[], limit:int=20):
    if len(tracks) == 0:
        _LOGGER.debug("Cannot add ZERO tracks to the queue!")
        return

    for track in tracks[:limit]:
        _LOGGER.debug("Adding " + track['name'] + " to the playback queue | " + track['uri'])
        spotify_client.add_to_queue(track['uri'])
        time.sleep(0.5)

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
    if elems[1].lower() == "user":
        elems = elems[0:1] + elems[3:]
        types = [ "playlist" ]
        _LOGGER.debug(f"Excluding user information from the Spotify URI validation. Only supported for playlists")

    # support playing a user's liked songs list (spotify:user:username:collection)
    if len(elems) == 2 and elems[1].lower() == "collection":
        return True

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
