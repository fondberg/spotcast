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
from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
)

from custom_components.spotcast.services.utils import (
    entity_from_target_selector,
)

LOGGER = getLogger(__name__)

ADD_TO_QUEUE_SCHEMA = vol.Schema({
    vol.Required("spotify_uris"): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional("account"): cv.string,
})


async def async_add_to_queue(hass: HomeAssistant, call: ServiceCall):
    """Service to add spotify uris to the playback queue"""
