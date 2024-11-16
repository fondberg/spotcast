"""Main module for the websocket endpoints"""

from types import MappingProxyType

from homeassistant.core import HomeAssistant
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import async_response

from custom_components.spotcast.websocket import (
    playlists_handler,
    devices_handler,
    accounts_handler,
    player_handler,
    cast_devices_handler,
    categories_handler,
)

WEBSOCKET_ENDPOINTS = MappingProxyType({
    playlists_handler.ENDPOINT: {
        "handler": playlists_handler.async_get_playlists,
        "schema": playlists_handler.SCHEMA,
    },
    devices_handler.ENDPOINT: {
        "handler": devices_handler.async_get_devices,
        "schema": devices_handler.SCHEMA,
    },
    accounts_handler.ENDPOINT: {
        "handler": accounts_handler.async_get_accounts,
        "schema": accounts_handler.SCHEMA,
    },
    player_handler.ENDPOINT: {
        "handler": player_handler.async_get_playback,
        "schema": player_handler.SCHEMA,
    },
    cast_devices_handler.ENDPOINT: {
        "handler": cast_devices_handler.async_get_cast_devices,
        "schema": cast_devices_handler.SCHEMA,
    },
    categories_handler.ENDPOINT: {
        "handler": categories_handler.async_get_categories,
        "schema": categories_handler.SCHEMA,
    },
})


async def async_setup_websocket(hass: HomeAssistant):
    """Registers the websocket endpoints"""

    for endpoint, data in WEBSOCKET_ENDPOINTS.items():
        websocket_api.async_register_command(
            hass=hass,
            command_or_handler=endpoint,
            handler=async_response(data["handler"]),
            schema=data["schema"],
        )
