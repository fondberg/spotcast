"""Module for the play category service

Functions:
    - async_play_category
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol
from random import choice


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.utils import (
    get_account_entry,
    copy_to_dict,
)
from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
    find_category,
)

LOGGER = getLogger(__name__)

PLAY_CATEGORY_SCHEMA = vol.Schema({
    vol.Optional("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("category"): cv.string,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_category(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing a random playlist from a browse
    category

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    # retreiving data from call
    account_id: str = call.data.get("account")
    category_str: str = call.data.get("category")
    extras: str = call.data.get("data")

    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    categories = await account.async_categories()

    category = find_category(categories, category_str)

    playlists = await account.async_category_playlists(category["id"])

    # remove dj playlist if present
    playlists = [x for x in playlists if x["uri"] != account.DJ_URI]

    # reduce size of aray if limit present
    if extras is not None and "limit" in extras:
        playlists = playlists[:extras["limit"]]

    playlist = choice(playlists)

    LOGGER.info(
        "Randomly Selected playlist `%s` from category `%s`",
        playlist["name"],
        category["name"],
    )

    call_data = copy_to_dict(call.data)
    call_data.pop("category")
    call_data["spotify_uri"] = playlist["uri"]
    call.data = ReadOnlyDict(call_data)

    await async_play_media(hass, call)
