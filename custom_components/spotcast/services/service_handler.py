"""Module containing a service handlers that pre parse service call
and redirecteds call service to the proper function

Classes:
    - ServiceHandler
"""

from logging import getLogger

from homeassistant.core import ServiceCall, HomeAssistant

from custom_components.spotcast.services.exceptions import (
    UnknownServiceError,
)

from custom_components.spotcast.services.const import SERVICE_HANDLERS

LOGGER = getLogger(__name__)


class ServiceHandler:
    """Handler for Service call that redirect service calls with added
    arguments

    Attributes:
        - hass(HomeAssistant): The Home Assistant Instance

    Methods:
        - async_relay_service_call
    """

    def __init__(self, hass: HomeAssistant):
        """Handler for Service call that redirect service calls with added
        arguments

        Args:
            - hass(HomeAssistant): The Home Assistant Instance
        """
        self.hass = hass

    async def async_relay_service_call(self, call: ServiceCall):
        """Relays a service call to the proper function with required
        arguments for the service call

        Args:
            - call(ServiceCall): The current service call to handle
        """

        service_name = call.service

        try:
            handler = SERVICE_HANDLERS[service_name]
        except KeyError as exc:
            raise UnknownServiceError(
                f"`{call.domain}.{service_name}` is not a known service to "
                "spotcast"
            ) from exc

        await handler(self.hass, call)
