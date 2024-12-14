"""Module for the search websocket api endpoint"""

import voluptuous as vol
from custom_components.spotcast.spotify.search_query import SearchQuery
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.spotify.utils import select_image_url
from custom_components.spotcast.websocket.utils import (
    websocket_wrapper,
    async_get_account,
)

ENDPOINT = "spotcast/search"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("query"): cv.string,
        # Playlist or song, default playlist
        vol.Optional("searchType"): cv.string,
        vol.Optional("limit"): cv.positive_int,
        vol.Optional("account"): cv.string,
    }
)


@websocket_wrapper
async def async_search_handler(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict,
):
    """Searches for playlists or tracks.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket
            connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    query = msg.get("query")
    search_type = msg.get("searchType", "playlist")
    limit = msg.get("limit", 10)

    account = await async_get_account(hass, account_id)

    query = SearchQuery(search=query, item_types=search_type)

    results = await account.async_search(
        query,
        limit,
    )

    results = results[f"{search_type}s"]

    formatted_results = []

    for item in results:

        images = item.get("images", [])

        formatted_results.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "uri": item.get("uri"),
            "description": item.get("description"),
            "icon": select_image_url(images),
        })

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_results),
            "account": account.id,
            f"{search_type}s": formatted_results,
        },
    )
