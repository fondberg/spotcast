"""Module for the add to queue service

Functions:
    - async_add_to_queue
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry
from custom_components.spotcast.services.exceptions import (
    NoActivePlaybackError
)

LOGGER = getLogger(__name__)

ADD_TO_QUEUE_SCHEMA = vol.Schema({
    vol.Required("spotify_uris"): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional("account"): cv.string,
})


async def async_add_to_queue(hass: HomeAssistant, call: ServiceCall):
    """Service to add spotify uris to the playback queue"""
    uris = call.data.get("spotify_uris")
    account_id = call.data.get("account")

    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    playback_state = await account.async_playback_state(force=True)

    if playback_state == {}:
        raise NoActivePlaybackError(
            "No active playback active for account `%s`. Active "
            "playback is required to add to queue",
            account.id
        )

    for uri in uris:
        await account.async_add_to_queue(uri)
