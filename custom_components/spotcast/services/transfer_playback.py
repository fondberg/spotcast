"""Module for the transfer_playback service

Functions:
    - async_transfer_playback
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
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

    # check if no active playback
    if playback_state == {} and account.last_playback_state == {}:
        raise ServiceValidationError(
            f"Account `{account.name}` has no known or active playback. "
            "Nothing to transfer"
        )

    call_data["spotify_uri"] = None

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
    last_playback_state = account.last_playback_state
    context_uri = last_playback_state["context"]["uri"]
    context_type = last_playback_state["context"]["type"]
