"""Module to define the play_media service"""

from logging import getLogger

from homeassistant.core import ServiceCall, HomeAssistant

from custom_components.spotcast.services.exceptions import (
    UnknownServiceError,
)
from custom_components.spotcast.services.play_media import async_play_media

LOGGER = getLogger(__name__)


class ServiceHandler:

    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def async_relay_service_call(self, call: ServiceCall):

        service_name = call.service

        services = {
            "play_media": async_play_media
        }

        try:
            await services[service_name](self.hass, call)
        except KeyError as exc:
            raise UnknownServiceError(
                f"`{call.domain}.{service_name}` is not a known service to "
                "spotcast"
            ) from exc
