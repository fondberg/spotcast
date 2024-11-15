"""Websocket Endpoint for getting the list of accounts"""

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper

ENDPOINT = "spotcast/accounts"
SCHEMA = vol.Schema({
    vol.Required("id"): cv.positive_int,
    vol.Required("type"): ENDPOINT,
})


@websocket_api.async_response
@websocket_wrapper
async def async_get_playback(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict
):
    """Gets a list playlists from an account

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - connection(ActiveConnection): the Active Websocket connection
            object
        - msg(dict): the message received through the websocket API
    """

    accounts: dict[str, SpotifyAccount]
    accounts = {x: y["account"] for x, y in hass.data[DOMAIN].items()}

    result = []

    for entry_id, account in accounts.items():
        result.append({
            "entry_id": entry_id,
            "spotify_id": account.id,
            "spotify_name": account.name,
            "is_default": account.is_default,
            "country": account.country,
        })

    connection.send_result(
        msg["id"],
        {
            "total": len(result),
            "accounts": accounts,
        },
    )
