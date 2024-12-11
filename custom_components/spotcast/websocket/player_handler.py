"""Websocket Endpoint for getting playback state"""

from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from custom_components.spotcast.websocket.utils import (
    websocket_wrapper,
    async_get_account,
)

ENDPOINT = "spotcast/player"
SCHEMA = vol.Schema({
    vol.Required("id"): cv.positive_int,
    vol.Required("type"): ENDPOINT,
    vol.Optional("account"): cv.string,
})


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

    account = await async_get_account(hass, account_id)

    playback_state = await account.async_playback_state(force=True)

    connection.send_result(
        msg["id"],
        {
            "account": account.id,
            "state": playback_state,
        },
    )
