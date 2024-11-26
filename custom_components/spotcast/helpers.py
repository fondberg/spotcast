from __future__ import annotations

import asyncio
import logging
import requests
import urllib.parse
import difflib
import random
import time
from functools import partial, wraps

import homeassistant.core as ha_core

# import for type inference
import spotipy
from spotipy import SpotifyException
from homeassistant.components.cast.media_player import CastDevice
from homeassistant.components.spotify.media_player import SpotifyMediaPlayer
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform

_LOGGER = logging.getLogger(__name__)


def get_spotify_media_player(
    hass: ha_core.HomeAssistant, spotify_user_id: str
) -> SpotifyMediaPlayer:
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
                except (AttributeError):
                    try:
                        entity_devices = entity.data.devices.data
                    except AttributeError:
                        entity_devices = entity.devices.data

                _LOGGER.debug(
                    f"get_spotify_devices: {entity.entity_id}: "
                    f"{entity.name}: %s",
                    entity_devices,
                )
                spotify_media_player = entity
                break

    if spotify_media_player:
        return spotify_media_player
    else:
        raise HomeAssistantError("Could not find spotify media player.")


def get_spotify_devices(
        spotify_media_player: SpotifyMediaPlayer,
        hass: HomeAssistant
):

    if spotify_media_player:
        # Need to come from media_player spotify's sp client due to
        # token issues
        asyncio.run_coroutine_threadsafe(
            spotify_media_player.devices.async_refresh(),
            hass.loop,
        ).result()

        spotify_devices = spotify_media_player.devices.data

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
                    f"get_cast_devices: {entity.entity_id}: "
                    f"{entity.name} cast info: % s",
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


def get_top_tracks(
    artistName: str,
    spotify_client: spotipy.Spotify,
    limit: int = 20,
    country: str = None,
):

    _LOGGER.debug("Searching for top tracks for the artist: %s", artistName)
    searchType = "artist"
    search = searchType + ":" + artistName

    artistUri = ""

    # get artist uri
    try:

        artist = spotify_client.search(
            q=search,
            limit=1,
            offset=0,
            type="artist",
            market=country,
        )["artists"]["items"][0]

        _LOGGER.debug("found artist %s: %s", artist["name"], artist["uri"])
        artistUri = artist["uri"]

    except IndexError:
        pass

    results = spotify_client.artist_top_tracks(artistUri)
    for track in results["tracks"][:10]:
        _LOGGER.debug("track    : " + track["name"])

    return results["tracks"]


def get_search_string(
    artistName: str,
    albumName: str,
    trackName: str,
    genreName: str,
    playlistName: str,
    showName: str,
    episodeName: str,
    audiobookName: str,
) -> str:
    search = []
    if not is_empty_str(artistName):
        search.append(f"artist:{artistName}")
        search.append(artistName)
    if not is_empty_str(albumName):
        search.append(f"album:{albumName}")
        search.append(albumName)
    if not is_empty_str(trackName):
        search.append(f"track:{trackName}")
        search.append(trackName)
    if not is_empty_str(genreName):
        search.append(f"genre:{genreName}")
        search.append(genreName)
    # if we are searching for a playlist, podcast, audiobook, we need
    # some search query which is probably just the text we are looking
    # for
    for item in [playlistName, showName, episodeName, audiobookName]:
        if not is_empty_str(item):
            search.append(item)

    return " ".join(search)


# "album", "artist", "playlist", "track", "show", "episode", "audiobook"
def get_types_string(
    artistName: str,
    albumName: str,
    trackName: str,
    playlistName: str,
    showName: str,
    episodeName: str,
    audiobookName: str,
) -> str:
    types = []
    if not is_empty_str(artistName):
        types.append("artist")
    if not is_empty_str(albumName):
        types.append("album")
    if not is_empty_str(trackName):
        types.append("track")
    if not is_empty_str(playlistName):
        types.append("playlist")
    if not is_empty_str(showName):
        types.append("show")
    if not is_empty_str(episodeName):
        types.append("episode")
    if not is_empty_str(audiobookName):
        types.append("audiobook")
    return ",".join(types)


def get_search_results(
    spotify_client: spotipy.Spotify,
    limit: int = 10,
    country: str = None,
    artistName: str = None,
    albumName: str = None,
    playlistName: str = None,
    trackName: str = None,
    showName: str = None,
    episodeName: str = None,
    audiobookName: str = None,
    genreName: str = None,
):
    _LOGGER.debug("using search query to find uri")
    searchResults = []

    if (
        not is_empty_str(artistName)
        and len(
            list(
                filter(
                    lambda x: not is_empty_str(x),
                    [
                        albumName,
                        playlistName,
                        trackName,
                        showName,
                        episodeName,
                        audiobookName,
                        genreName,
                    ],
                )
            )
        )
        == 0
    ):
        searchResults = get_top_tracks(artistName, spotify_client)
        _LOGGER.debug("Playing top tracks for artist: %s",
                      searchResults[0]["name"])
        return searchResults
    else:
        searchString = get_search_string(
            artistName=artistName,
            albumName=albumName,
            trackName=trackName,
            genreName=genreName,
            playlistName=playlistName,
            showName=showName,
            episodeName=episodeName,
            audiobookName=audiobookName,
        )

        searchTypes = get_types_string(
            artistName=artistName,
            albumName=albumName,
            trackName=trackName,
            playlistName=playlistName,
            showName=showName,
            episodeName=episodeName,
            audiobookName=audiobookName,
        )
        searchResults = spotify_client.search(
            q=searchString,
            limit=limit,
            offset=0,
            type=searchTypes,
            market=country
        )

        compiledResults = []
        if "tracks" in searchResults:
            for item in searchResults["tracks"]["items"]:
                compiledResults.append(item)
        if "albums" in searchResults:
            for item in searchResults["albums"]["items"]:
                compiledResults.append(item)
        if "playlists" in searchResults:
            for item in searchResults["playlists"]["items"]:
                compiledResults.append(item)
        if "shows" in searchResults:
            for item in searchResults["shows"]["items"]:
                compiledResults.append(item)
        if "audiobooks" in searchResults:
            for item in searchResults["audiobooks"]["items"]:
                compiledResults.append(item)
        if "episodes" in searchResults:
            for item in searchResults["episodes"]["items"]:
                compiledResults.append(item)

        _LOGGER.debug(
            "Found %d results for %s. First Track name: %s",
            len(compiledResults),
            searchString,
            compiledResults[0]["name"],
        )

        return compiledResults


def search_tracks(
    search: str,
    spotify_client: spotipy.Spotify,
    appendToQueue: bool = False,
    shuffle: bool = False,
    startRandom: bool = False,
    limit: int = 20,
    artistName: str = None,
    country: str = None,
):
    results = get_search_results(
        search, spotify_client, artistName, limit, country)
    if len(results) > 0:
        firstResult = [results[0]]
        if not startRandom:
            results = results[1:limit]
        if shuffle:
            random.shuffle(results)
        if not startRandom:
            results = firstResult + results

    return results


def add_tracks_to_queue(
    spotify_client: spotipy.Spotify, tracks: list = [], limit: int = 20
):
    filtered = list(filter(lambda x: isinstance(x, dict) and x.get("type") == "track", tracks))

    if len(filtered) == 0:
        _LOGGER.debug("Cannot add ZERO tracks to the queue!")
        return

    for track in filtered[:limit]:
        _LOGGER.debug(
            "Adding " + track["name"] +
            " to the playback queue | " + track["uri"]
        )

        max_attemps = 5
        backoff_rate = 1.2
        delay = 1
        current_attempt = 0

        while True:
            try:
                spotify_client.add_to_queue(track["uri"])
            except SpotifyException as exc:

                if current_attempt >= max_attemps:
                    raise HomeAssistantError(
                        "Coulddn't addd song to queue"
                    ) from exc

                _LOGGER.warning("Couldn't add song to queue retrying")

                time.sleep(delay)
                current_attempt += 1
                delay *= backoff_rate

                continue

            break

        time.sleep(0.5)


def get_random_playlist_from_category(
    spotify_client: spotipy.Spotify,
    category: str,
    country: str = None,
    limit: int = 20,
) -> str:

    if country is None:

        _LOGGER.debug(
            f"Get random playlist among {limit} playlists from category "
            f"{category}, no country specified."
        )

    else:

        _LOGGER.debug(
            f"Get random playlist among {limit} playlists from category "
            f"{category} in country {country}"
        )

        # validate category and country are valid entries
        if country.upper() not in spotify_client.country_codes:
            _LOGGER.error(f"{country} is not a valid country code")
            return None

    # get list of playlist from category and localisation provided
    try:
        playlists = spotify_client.category_playlists(
            category_id=category, country=country, limit=limit
        )["playlists"]["items"]
    except spotipy.exceptions.SpotifyException as e:
        _LOGGER.error(e.msg)
        return None

    # choose one at random
    chosen = random.choice(playlists)

    _LOGGER.debug(
        f"Chose playlist {chosen['name']}({chosen['uri']}) from category "
        f"{category}."
    )

    return chosen["uri"]


def url_to_spotify_uri(url: str) -> str:
    """
    Convert a spotify web url (e.g. https://open.spotify.com/track/XXXX) to
    a spotify-style URI (spotify:track:XXXX). Returns None on error.
    """

    o: urllib.parse.ParseResult
    # will raise ValueError if URL is invalid
    o = urllib.parse.urlparse(url)

    if o.hostname != "open.spotify.com":
        raise ValueError(
            'Spotify URLs must have a hostname of "open.spotify.com"')

    path = o.path.split("/")
    if len(path) != 3:
        raise ValueError(
            'Spotify URLs must be of the form "https://open.spotify.com/<kind>/<target>"')

    return f'spotify:{path[1]}:{path[2]}'


def is_valid_uri(uri: str) -> bool:

    # list of possible types
    types = ["artist", "album", "track", "playlist", "show", "episode"]

    # split the string
    elems = uri.split(":")

    # validate number of sub elements
    if elems[1].lower() == "user":
        elems = elems[0:1] + elems[3:]
        types = ["playlist"]
        _LOGGER.debug(
            "Excluding user information from the Spotify URI validation. Only"
            " supported for playlists"
        )

    # support playing a user's liked songs list
    # (spotify:user:username:collection)
    if len(elems) == 2 and elems[1].lower() == "collection":
        return True

    if len(elems) != 3:
        _LOGGER.error(
            f"[{uri}] is not a valid URI. The format should be "
            "[spotify:<type>:<unique_id>]"
        )
        return False

    # check correct format of the sub elements
    if elems[0].lower() != "spotify":
        _LOGGER.error(
            f"This is not a valid Spotify URI. This should start with "
            f"[spotify], but instead starts with [{elems[0]}]"
        )
        return False

    if elems[1].lower() not in types:
        _LOGGER.error(
            f"{elems[1]} is not a valid type for Spotify request. Please "
            f"make sure to use the following list {str(types)}"
        )
        return False

    if "?" in elems[2]:
        _LOGGER.warning(
            f"{elems[2]} contains query character. This should work, but you"
            " should probably remove it and anything after."
        )

    # return True if all test passes
    return True


def is_empty_str(string: str) -> bool:
    return string is None or string.strip() == ""
