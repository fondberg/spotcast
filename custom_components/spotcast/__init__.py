"""Spotcast Integration - Chromecast to Spotify integrator"""

from logging import getLogger
from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform

from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.services import ServiceHandler
from custom_components.spotcast.services.play_media import PLAY_MEDIA_SCHEMA

__version__ = "4.0.0-beta"


LOGGER = getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    LOGGER.info(
        "Loaded spotify account `%s`. Set as default: %s",
        account.id,
        account.is_default
    )

    try:
        await account.async_ensure_tokens_valid()
    except ClientError as exc:
        raise ConfigEntryNotReady from exc

    hass.data.setdefault(DOMAIN, {})[account.id] = entry

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    service_handler = ServiceHandler(hass)

    hass.services.async_register(
        domain=DOMAIN,
        service="play_media",
        service_func=service_handler.async_relay_service_call,
        schema=PLAY_MEDIA_SCHEMA,
    )

    return True
