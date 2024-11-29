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
        vol.optional("searchType"): cv.string, # Playlist or song, default playlist
        vol.Optional("limit"): cv.positive_int,
    }
)

@websocket_wrapper
async def search_handler(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
):
    """Searches for a playlist or song.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    query = msg.get("url")
    searchType = msg.get("searchType", "playlist")
    limit = msg.get("limit", 10)

    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    # prepend view/ to the url
    url = f"view/{url}"

    result = await account.async_search(
        query: query,
        searchType: searchType,
        limit: limit,
    )

    formatted_results = [
        {
            "id": item["id"],
            "name": item["name"],
            "icon": item["images"][0]["url"]
            if "images" in item and len(item["images"]) > 0
            else None,
        }
        for item in result[searchType]
        if "id" in item  # Only include playlists with an 'id'
    ]

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_results),
            "account": account_id,
            "playlists": formatted_results,
        },
    )
