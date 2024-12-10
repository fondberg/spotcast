import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper

ENDPOINT = "spotcast/liked_media"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Optional("account"): cv.string,
    }
)


@websocket_wrapper
async def async_liked_media(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
):
    """Gets the liked media of a user.

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")

    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    liked_media = await account.async_liked_songs()

    connection.send_result(
        msg["id"],
        {
            "total": len(liked_media),
            "account": account_id,
            "tracks": liked_media,
        },
    )
