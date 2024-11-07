"""Module for the play media service

Functions:
    - async_play_media
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.services.utils import EXTRAS_SCHEMA

LOGGER = getLogger(__name__)

PLAY_DJ_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_dj(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    call.data["spotify_uri"] = SpotifyAccount.DJ_URI
    extras = call.data.get("data")

    if extras is not None:
        extras = _clean_extras(extras)

    await async_play_media(hass, call)


def _clean_extras(extras: dict) -> dict:
    """Cleans the extras dictionary before calling the async_play_media
    """
    keep = ("volume",)
    result = {}

    for key, value in extras.items():

        if key not in keep:
            LOGGER.debug(
                "Ignoring extra parameter `%s`. Irrelevant for DJ",
                key,
            )
            continue

        result[key] = value

    return value
