"""Module for the transfer_playback service

Functions:
    - async_transfer_playback
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol


from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.services.utils import EXTRAS_SCHEMA
from custom_components.spotcast.utils import copy_to_dict

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

    call_data = copy_to_dict(call.data)
    call_data["spotify_uri"] = None
    call.data = ReadOnlyDict(call_data)

    await async_play_media(hass, call)
