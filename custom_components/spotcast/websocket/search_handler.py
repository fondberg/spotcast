import voluptuous as vol
from custom_components.spotcast.spotify.search_query import SearchQuery
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper
from custom_components.spotcast.spotify.utils import select_image_url

ENDPOINT = "spotcast/search"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("query"): cv.string,
        vol.Optional("searchType"): cv.string,  # Playlist or song, default playlist
        vol.Optional("limit"): cv.positive_int,
        vol.Optional("account"): cv.string,
    }
)


@websocket_wrapper
async def async_search_handler(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
):
    """Searches for playlists or tracks.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    query = msg.get("query")
    searchType = msg.get("searchType", "playlist")
    limit = msg.get("limit", 10)

    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    query = SearchQuery(search=query, item_type=searchType)

    results = await account.async_search(
        query,
        limit,
    )

    formatted_results = [
        {
            "id": result.get("id", None),
            "name": result["name"],
            "href": result["href"],
            "icon": result["images"][0]["url"]
            if "images" in result and len(result["images"]) > 0
            else None,
        }
        for result in results
    ]

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_results),
            "account": account_id,
            f"{searchType}s": formatted_results,
        },
    )