"""Module for the play media service

Functions:
    - async_play_media
"""

from logging import getLogger
from random import randint

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
import voluptuous as vol


from custom_components.spotcast.media_player import SpotifyDevice
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry
from custom_components.spotcast.spotify.utils import url_to_uri
from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
)

from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
    entity_from_target_selector
)

LOGGER = getLogger(__name__)

PLAY_MEDIA_SCHEMA = vol.Schema({
    vol.Optional("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("spotify_uri"): url_to_uri,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_media(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """
    uri: str = call.data.get("spotify_uri")
    account_id: str = call.data.get("account")
    media_players: dict[str, list] = call.data.get("media_player")
    extras: dict[str] = call.data.get("data")

    if extras is None:
        extras = {}

    entry = get_account_entry(hass, account_id)
    entity_id = None

    if media_players is not None:
        entity_id = entity_from_target_selector(hass, media_players)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    # check for track uri and switch to album with offset if necessary
    if uri is None:
        pass
    elif uri.startswith("spotify:track:"):

        uri, index = await async_track_index(account, uri)
        LOGGER.debug(
            "Switching context to song's album `%s`, with offset %d",
            uri,
            index,
        )
        extras["offset"] = index - 1
    elif extras.get("random", False):
        extras["offset"] = await async_random_index(account, uri)

    if entity_id is not None:
        LOGGER.debug("Getting %s from home assistant", entity_id)
        media_player = await async_media_player_from_id(
            hass=hass,
            account=account,
            entity_id=entity_id
        )
    elif (playback_state := await account.async_playback_state(force=True))\
            != {}:
        media_player = SpotifyDevice(account, playback_state["device"])
    else:
        raise ServiceValidationError(
            "No active playback available. Provide a target"
        )

    LOGGER.info(
        "Playing `%s` on `%s` for account `%s`",
        uri,
        media_player.name,
        account.id
    )

    await account.async_play_media(media_player.id, uri, **extras)
    await account.async_apply_extras(media_player.id, extras)


async def async_track_index(
    account: SpotifyAccount,
    uri: str
) -> tuple[str, int]:
    """Returns the uri of the album and the index that would play the
    uri provided in the context of the album

    Args:
        - account(SpotifyAccount): the account used to fetch track
            information
        - uri(str): A track URI

    Returns:
        - tuple[str, int]: A tuple containing the album uri of the
            track and its index in the album (counting multi disc
            albums)
    """
    track_info = await account.async_get_track(uri)
    album_uri = track_info["album"]["uri"]

    # returns track number, when part of album
    if track_info["disc_number"] == 1:
        return album_uri, track_info["track_number"]

    album_info = await account.async_get_album(album_uri)

    album_songs = [x["uri"] for x in album_info["tracks"]["items"]]

    return album_uri, album_songs.index(uri) + 1


async def async_random_index(account: SpotifyAccount, uri: str) -> int:
    """Returns a random index for starting the context at. Must be an
    artist, album or playlist

    Args:
        - account(SpotifyAccount): the account used for fetching
            context info
        - uri(str): the uri of the context to start at a random index

    Result:
        - int: a random index between 0 and the number of items in the
            context uri - 1
    """

    if uri.startswith("spotify:album:"):
        album = await account.async_get_album(uri)
        count = album["total_tracks"]
    elif uri.startswith("spotify:playlist:"):
        playlist = await account.async_get_playlist(uri)
        count = playlist["tracks"]["total"]
    elif uri == account.liked_songs_uri:
        count = await account.async_liked_songs_count()
    else:
        raise ServiceValidationError(
            f"{uri} is not compatible with random start track"
        )

    return randint(0, count-1)
