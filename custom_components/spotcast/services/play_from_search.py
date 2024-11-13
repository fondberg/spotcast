"""Module for the play_from_search service

Functions:
    - async_play_from_search
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.services.play_custom_context import (
    async_play_custom_context
)
from custom_components.spotcast.services.utils import EXTRAS_SCHEMA
from custom_components.spotcast.spotify.search_query import SearchQuery
from custom_components.spotcast.utils import (
    get_account_entry,
    copy_to_dict
)

LOGGER = getLogger(__name__)

PLAY_FROM_SEARCH_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("search_term"): cv.string,
    vol.Required("item_type"): vol.In(SearchQuery.ALLOWED_ITEM_TYPE),
    vol.Optional("tags"): vol.All(
        cv.ensure_list, [vol.In(SearchQuery.ALLOWED_TAGS)]
    ),
    vol.Optional("filters"): vol.Schema({
        vol.Optional("album"): cv.string,
        vol.Optional("artist"): cv.string,
        vol.Optional("track"): cv.string,
        vol.Optional("year"): cv.string,
        vol.Optional("upc"): cv.string,
        vol.Optional("isrc"): cv.string,
        vol.Optional("genre"): cv.string,
    }),
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})

MULTI_ITEMS_TYPE = ("track", "episode")


async def async_play_from_search(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media from a search result

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    # extract the data fron the call
    search_term = call.data.get("search_term")
    item_type = call.data.get("item_type")
    tags = call.data.get("tags")
    filters = call.data.get("filters")
    account_id = call.data.get("account")
    extras = call.data.get("data")

    # sets the limit according to item type or extras limit. Defaults
    # to 20
    limit = 20

    if item_type not in MULTI_ITEMS_TYPE:
        limit = 1
    elif extras is not None and "limit" in extras:
        limit = extras["limit"]

    # get account
    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    # build search query
    query = SearchQuery(search_term, item_type, filters, tags)

    search_result = await account.async_search(query, limit)

    call_data = copy_to_dict(call.data)

    for key in ("search_term", "item_type", "tags", "filters"):
        if key in call_data:
            call_data.pop(key)

    if item_type in MULTI_ITEMS_TYPE:
        tracks = [x["uri"] for x in search_result]
        LOGGER.debug(
            "Playing %d songs fron search `%s`",
            len(tracks),
            search_term,
        )

        call_data["tracks"] = tracks
        service_function = async_play_custom_context

    else:

        context_uri = search_result[0]["uri"]
        LOGGER.debug(
            "Playing uir `%s` as a result of search `%s`",
            context_uri,
            search_term
        )

        call_data["spotify_uri"] = context_uri
        service_function = async_play_media

    call.data = ReadOnlyDict(call_data)
    await service_function(hass, call)
