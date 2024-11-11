"""Module for the play dj service

Functions:
    - async_play_dj
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
    clean_extras,
)
from custom_components.spotcast.utils import copy_to_dict

LOGGER = getLogger(__name__)

PLAY_DJ_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})

EXTRAS_TO_KEEP = ("volume",)


async def async_play_dj(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    extras = call.data.get("data")

    if extras is not None:
        extras = clean_extras(extras, EXTRAS_TO_KEEP)

    call_data = copy_to_dict(call.data)
    call_data["spotify_uri"] = SpotifyAccount.DJ_URI
    call_data["data"] = extras
    call.data = ReadOnlyDict(call_data)

    await async_play_media(hass, call)
