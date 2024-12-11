import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.spotify.utils import select_image_url
from custom_components.spotcast.websocket.utils import (
    websocket_wrapper,
    async_get_account,
)

ENDPOINT = "spotcast/view"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("name"): cv.string,
        vol.Optional("account"): cv.string,
        vol.Optional("limit"): cv.positive_int,
        vol.Optional("language"): vol.All(cv.string, vol.Length(min=2, max=2)),
    }
)


@websocket_wrapper
async def async_view_handler(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict,
):
    """Gets a list of playlists from a specified account.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    name = msg.get("name")
    limit = msg.get("limit")
    language = msg.get("locale")

    account = await async_get_account(hass, account_id)

    # prepend views/ to the url
    url = f"views/{name}"

    raw_playlists = await account.async_view(
        url=url,
        language=language,
        limit=limit,
    )

    formatted_playlists = []

    for playlist in raw_playlists:
        images = playlist.get("images", [])

        formatted_playlists.append({
            "id": playlist.get("id"),
            "name": playlist.get("name"),
            "uri": playlist.get("uri"),
            "description": playlist.get("description"),
            "icon": select_image_url(images)
        })

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_playlists),
            "account": account.id,
            "playlists": formatted_playlists,
        },
    )
