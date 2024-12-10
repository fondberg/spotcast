"""Module for the play saved episodes service

Functions:
    - async_play_saved_episodes
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import (
    get_account_entry,
    copy_to_dict,
)
from custom_components.spotcast.services.play_custom_context import (
    async_play_custom_context
)
from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
)

LOGGER = getLogger(__name__)

PLAY_SAVED_EPISODES = vol.Schema({
    vol.Optional("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_saved_episodes(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing the saved podcast episode on the user
    account

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    account_id = call.data.get("account")
    extras = call.data.get("data", {})

    limit = extras.get("limit")

    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    episodes = await account.async_saved_episodes(limit)
    episode_uris = [x["episode"]["uri"] for x in episodes]

    call_data = copy_to_dict(call.data)
    call_data["tracks"] = episode_uris
    call.data = ReadOnlyDict(call_data)

    await async_play_custom_context(hass, call)
