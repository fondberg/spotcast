"""Websocket Endpoint for getting playback state"""

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper

ENDPOINT = "spotcast/player"
SCHEMA = vol.Schema({
    vol.Required("id"): cv.positive_int,
    vol.Required("type"): ENDPOINT,
    vol.Optional("account"): cv.string,
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

    account_id = msg.get("account")
    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account)

    playback_state = await account.async_playback_state(force=True)

    connection.send_result(
        msg["id"],
        playback_state,
    )
