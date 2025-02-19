"""Module for the playng podcast

Functions:
    - async_play_podcast
"""

from logging import getLogger

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant, ServiceCall

from custom_components.spotcast.spotify.utils import url_to_uri
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
    """Service to start playing a podcast

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """
    uri: str = call.data.get("spotify_uri")
    account_id: str = call.data.get("account")
    media_player: dict[str, list] = call.data.get("media_player")
    extras: dict[str] = call.data.get("data")

    if extras is None:
        extras = {}
