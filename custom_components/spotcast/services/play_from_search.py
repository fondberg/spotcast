"""Module for the play_from_search service

Functions:
    - async_play_from_search
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.util.read_only_dict import ReadOnlyDict
import voluptuous as vol
from rapidfuzz import fuzz


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services.play_media import async_play_media
from custom_components.spotcast.services.utils import EXTRAS_SCHEMA
from custom_components.spotcast.spotify.search_query import SearchQuery
from custom_components.spotcast.utils import (
    get_account_entry,
    copy_to_dict
)

LOGGER = getLogger(__name__)

PLAY_FROM_SEARCH_SCHEMA = vol.Schema({
    vol.Optional("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("search_term"): cv.string,
    vol.Required("item_types"): vol.All(
        cv.ensure_list,
        [vol.In(SearchQuery.ALLOWED_ITEM_TYPE)],
    ),
    vol.Optional("tags"): vol.All(
        cv.ensure_list,
        [vol.In(SearchQuery.ALLOWED_TAGS)],
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

ITEM_TYPE_PRIORITY = (
    "artists",
    "tracks",
    "albums",
    "playlists",
    "audiobooks",
    "shows",
    "episodes"
)


async def async_play_from_search(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media from a search result

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    # extract the data fron the call
    search_term = call.data.get("search_term")
    item_types = call.data.get("item_types")
    tags = call.data.get("tags")
    filters = call.data.get("filters")
    account_id = call.data.get("account")
    extras = call.data.get("data", {})

    # sets the limit according to item type or extras limit. Defaults
    # to 20
    limit = extras.get("limit", 1)

    # get account
    entry = get_account_entry(hass, account_id)
    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    # build search query
    query = SearchQuery(search_term, item_types, filters, tags)
    search_result = await account.async_search(query, limit)

    call_data = copy_to_dict(call.data)

    # remove unwanted items from call data
    for key in ("search_term", "item_type", "tags", "filters"):
        if key in call_data:
            call_data.pop(key)

    best_candidate = get_best_candidate(search_term, search_result)
    items = search_result[best_candidate]

    context_uri = items[0]["uri"]
    LOGGER.debug(
        "Playing uir `%s` as a result of search `%s`",
        context_uri,
        search_term
    )

    call_data["spotify_uri"] = context_uri

    call.data = ReadOnlyDict(call_data)
    await async_play_media(hass, call)


def get_best_candidate(
        search_term: str,
        search_result: dict[str, list[dict]]
) -> str:
    """Returns the best candidate for a search query according to
    the item in each category provided

    Args:
        - search_term(str): the term used for the search query
        - serach_result(dict[str, list[dict]]): the result from the
            search query

    Returns:
        - str: returns the item type selected as best candidate
    """

    best_ratio = 0
    best_candidate = None

    for key in ITEM_TYPE_PRIORITY:

        if key not in search_result or len(search_result[key]) == 0:
            continue

        items = search_result[key]

        candidate = items[0]["name"]
        ratio = fuzz.partial_ratio(search_term, candidate)

        if ratio > best_ratio:
            best_ratio = ratio
            best_candidate = key

    return best_candidate
