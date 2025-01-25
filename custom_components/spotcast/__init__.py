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
from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.const import Platform

from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.services import ServiceHandler
from custom_components.spotcast.services.const import SERVICE_SCHEMAS
from custom_components.spotcast.sessions.exceptions import (
    TokenRefreshError,
    InternalServerError,
)
from custom_components.spotcast.websocket import async_setup_websocket
from custom_components.spotcast.config_flow import DEFAULT_OPTIONS

__version__ = "5.0.0-b25"


LOGGER = getLogger(__name__)
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.MEDIA_PLAYER,
]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Yaml base setup. Triggers config flow import"""

    try:
        yaml_config = config[DOMAIN]
    except KeyError:
        return True

    # ensure minimal format required for import
    for key in ("sp_dc", "sp_key"):
        if key not in yaml_config:
            LOGGER.error(
                "Missing key `%s` in Spotcast configuration. Import to UI "
                "impossible. Aborting",
                key
            )
            return False

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data=yaml_config,
        )
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    # ensure default options
    updated_options = DEFAULT_OPTIONS | entry.options

    if updated_options != entry.options:
        hass.config_entries.async_update_entry(entry, options=updated_options)

    # because of circular depoendency
    from custom_components.spotcast.spotify.account import SpotifyAccount  # pylint: disable=C0415

    try:

        account = await SpotifyAccount.async_from_config_entry(
            hass=hass,
            entry=entry,
        )

        LOGGER.info(
            "Loaded spotify account `%s`. Set as default: %s",
            account.id,
            account.is_default
        )

        await account.async_ensure_tokens_valid()

    except TokenRefreshError as exc:
        raise ConfigEntryAuthFailed() from exc
    except InternalServerError as exc:
        raise ConfigEntryNotReady(f"{exc.code} - {exc.message}") from exc

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

    await async_setup_websocket(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unloads the Spotcast config entry"""
    LOGGER.info("Unloading Spotcast entry `%s`", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if not unload_ok:
        return False

    entry_data = hass.data[DOMAIN].get(entry.entry_id)
    listener = entry_data.get("device_listener")

    if listener is not None:
        listener()

    hass.data[DOMAIN].pop(entry.entry_id)

    # check if no entry remaining
    if len(hass.data[DOMAIN]) == 0:
        LOGGER.info("Last Spotcast Entry removed. Unloading services")

        for service in SERVICE_SCHEMAS:
            hass.services.async_remove(DOMAIN, service)

    return True
