"""Module for the play liked_songs service

Functions:
    - async_play_liked_songs
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.utils import (
    get_account_entry,
    read_only_dict_to_standard
)
from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
)

LOGGER = getLogger(__name__)

PLAY_LIKED_SONGS_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_liked_songs(hass: HomeAssistant, call: ServiceCall):
    """Service to start the play liked songs playlist for an account

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    account_id: str = call.data.get("account")
    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    call_data = read_only_dict_to_standard(call.data)
    call_data["spotify_uri"] = account.liked_songs_uri
    call.data = ReadOnlyDict(call_data)

    await async_play_media(hass, call)
