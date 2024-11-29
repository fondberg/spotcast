import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper
from custom_components.spotcast.spotify.utils import select_image_url

ENDPOINT = "spotcast/view"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("url"): cv.string,
        vol.Optional("limit"): cv.positive_int,
        vol.Optional("locale"): cv.string,
        vol.Optional("platform"): cv.string,
        vol.Optional("types"): cv.string,
        vol.Optional("account"): cv.string,
    }
)

@websocket_wrapper
async def view_handler(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
):
    """Gets a list of playlists from a specified account.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    url = msg.get("url")
    limit = msg.get("limit", 10)
    locale = msg.get("locale", "en_US")

    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    # prepend view/ to the url
    url = f"view/{url}"

    playlists = await account.async_view(
        url=url,
        limit=limit,
        locale=locale,
        types=types,
    )

    formatted_playlists = [
        {
            "id": playlist["id"],
            "name": playlist["name"],
            "icon": playlist["images"][0]["url"]
            if "images" in playlist and len(playlist["images"]) > 0
            else None,
        }
        for playlist in playlists["content"]["items"]
        if "id" in playlist  # Only include playlists with an 'id'
    ]

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_playlists),
            "account": account_id,
            "playlists": formatted_playlists,
        },
    )
