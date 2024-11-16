"""Websocket Endpoint for getting chromecast devices"""

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.websocket.utils import websocket_wrapper
from custom_components.spotcast.media_player.utils import (
    async_entities_from_integration,
    CastDevice,
)

ENDPOINT = "spotcast/castdevices"
SCHEMA = vol.Schema({
    vol.Required("id"): cv.positive_int,
    vol.Required("type"): ENDPOINT,
})


@websocket_wrapper
async def async_get_cast_devices(
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

    entities: dict[str, CastDevice] = await async_entities_from_integration(
        hass,
        "cast",
        ["media_player"],
    )

    devices = []

    for id, entity in entities.items():

        cast_info = entity._cast_info.cast_info

        devices.append({
            "entity_id": id,
            "uuid": str(cast_info.uuid),
            "model_name": cast_info.model_name,
            "friendly_name": cast_info.friendly_name,
            "manufacturer": cast_info.manufacturer,
        })

    connection.send_result(
        msg["id"],
        {
            "total": len(devices),
            "devices": devices
        },
    )
