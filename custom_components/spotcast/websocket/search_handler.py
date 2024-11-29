import voluptuous as vol
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
        vol.Optional("searchType"): cv.string, # Playlist or song, default playlist
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

    result = await account.async_search(
        query,
        searchType,
        limit,
    )

    formatted_results = [
        {
            "id": item["id"],
            "name": item["name"],
            "icon": item["images"][0]["url"]
            if "images" in item and len(item["images"]) > 0
            else None,
        }
        for item in result[f"{searchType}s"]
        if "id" in item
    ]

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_results),
            "account": account_id,
            f"{searchType}s": formatted_results,
        },
    )
