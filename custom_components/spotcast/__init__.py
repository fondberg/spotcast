"""Spotcast Integration - Chromecast to Spotify integrator

Functions:
    - async_setup_entry

Constants:
    - PLATFORMS(list): List of platforms implemented in this
        integration
    - DOMAIN(str): name of the domain of the integration
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform

from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.services import ServiceHandler
from custom_components.spotcast.services.const import SERVICE_SCHEMAS
from custom_components.spotcast.sessions.exceptions import TokenRefreshError

__version__ = "4.0.0-a0"


LOGGER = getLogger(__name__)
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.MEDIA_PLAYER,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """
    # because of circular depoendency
    from custom_components.spotcast.spotify.account import SpotifyAccount

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    LOGGER.info(
        "Loaded spotify account `%s`. Set as default: %s",
        account.id,
        account.is_default
    )

    try:
        await account.async_ensure_tokens_valid()
    except TokenRefreshError as exc:
        raise ConfigEntryNotReady from exc

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    service_handler = ServiceHandler(hass)

    for service, schema in SERVICE_SCHEMAS.items():

        LOGGER.debug("Registering service %s.%s", DOMAIN, service)

        hass.services.async_register(
            domain=DOMAIN,
            service=service,
            service_func=service_handler.async_relay_service_call,
            schema=schema,
        )

    return True
