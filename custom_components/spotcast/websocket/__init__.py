"""Main module for the websocket endpoints"""

from types import MappingProxyType

from homeassistant.core import HomeAssistant
from homeassistant.components import websocket_api

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.websocket import (
    playlist_handler,
    devices_handler,
    accounts_handler,
    player_handler,
)

WEBSOCKET_ENDPOINTS = MappingProxyType({
    playlist_handler.ENDPOINT: {
        "handler": playlist_handler.async_get_playlist,
        "schema": playlist_handler.SCHEMA,
    },
    devices_handler.ENDPOINT: {
        "handler": devices_handler.async_get_devices,
        "schema": devices_handler.SCHEMA,
    },
    accounts_handler.ENDPOINT: {
        "handler": accounts_handler.async_get_playback,
        "schema": accounts_handler.SCHEMA,
    },
    player_handler.ENDPOINT: {
        "handler": player_handler.async_get_playback,
        "schema": player_handler.SCHEMA,
    }
})


async def async_setup_websocket(hass: HomeAssistant):
    """Registers tje websocket endpoints"""

    hass.data[DOMAIN].get

    for endpoint, data in WEBSOCKET_ENDPOINTS.items():
        websocket_api.async_register_command(
            hass=hass,
            command_or_handler=endpoint,
            handler=data["handler"],
            schema=data["schema"],
        )
