"""Module for the transfer_playback service

Functions:
    - async_transfer_playback
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
from homeassistant.exceptions import ServiceValidationError
import voluptuous as vol


from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.services.play_media import (
    async_play_media,
    async_track_index,
)
from custom_components.spotcast.services.utils import EXTRAS_SCHEMA
from custom_components.spotcast.utils import copy_to_dict, get_account_entry

LOGGER = getLogger(__name__)

TRANSFER_PLAYBACK_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_transfer_playback(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    # get the current playback
    account_id = call.data.get("account")

    entry = get_account_entry(hass, account_id)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    playback_state = await account.async_playback_state(force=True)
    call_data = copy_to_dict(call.data)
    call_data["data"] = call_data.get("data", {})

    # check if no active playback
    if playback_state == {} and account.last_playback_state == {}:
        LOGGER.warning("No known playback state. Defaults back to liked songs")
        call_data["spotify_uri"] = account.liked_songs_uri
    elif playback_state != {}:
        call_data["spotify_uri"] = None
    else:
        call_data = await async_rebuild_playback(call_data, account)

    call.data = ReadOnlyDict(call_data)

    await async_play_media(hass, call)


async def async_rebuild_playback(
    call_data: dict,
    account: SpotifyAccount,
) -> dict:
    """Adds detail to the service call to restart the playback from
    the last known playback state

    Args:
        - call_data(dict): the data part of the service call
        - account(SpotifyAccount): the spotify account to rebuild
            playback from

    Return:
        - dict: the call_data modified with the last known state
            information
    """
    last_playback_state: dict = account.last_playback_state
    context_uri: str = last_playback_state["context"]["uri"]
    context_type: str = last_playback_state["context"]["type"]
    extras = call_data.get("data", {})

    # set the context_uri in the call_data
    call_data["spotify_uri"] = context_uri

    # set extras if not set by user
    if extras.get("repeat") is None:
        extras["repeat"] = last_playback_state["repeat_state"]

    if extras.get("shuffle") is None:
        extras["shuffle"] = last_playback_state["shuffle_state"]

    if extras.get("position") is None:
        extras["position"] = last_playback_state["progress_ms"]/1000

    # ensure modification are set in main call data
    call_data["data"] = extras

    if extras.get("offset") is not None:
        return call_data

    current_item = last_playback_state["item"]
    track_index = 0

    # set the offset according to the context type
    if context_type == "album":
        try:
            track_index = await async_track_index(account, current_item["uri"])
            track_index = track_index[1] - 1
        except ValueError:
            pass
    # change the context to the episode if context is show
    elif context_type == "show":
        call_data["spotify_uri"] = current_item["uri"]

    # all remaining case that rely on fetching a list of items and
    # finding the current uri in the list
    elif context_type in ("playlist", "collection"):

        tracks = []

        if context_type == "playlist":
            tracks = await account.async_get_playlist_tracks(context_uri)
            tracks = [x["track"]["uri"] for x in tracks]
        else:
            tracks = await account.async_liked_songs()

        try:
            track_index = tracks.index(current_item["uri"])
        except ValueError:
            pass

    call_data["data"]["offset"] = track_index
    return call_data
