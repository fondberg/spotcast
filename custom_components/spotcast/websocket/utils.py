"""Module for websoket API utility functions"""

from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection
from homeassistant.exceptions import ServiceValidationError, HomeAssistantError

HANDLED_EXCEPTIONS = (ServiceValidationError, HomeAssistantError)


def websocket_wrapper(func: callable):

    async def wrapper(
        hass: HomeAssistant,
        connection: ActiveConnection,
        msg: dict
    ):
        try:
            await func(hass, connection, msg)
        except HANDLED_EXCEPTIONS as exc:
            connection.send_error(msg["id"], type(exc).__name__, str(exc))

    return wrapper
