from logging import getLogger
from aiohttp import ClientError
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.spotcast.spotify import SpotifyAccount


DOMAIN = "spotcast"
LOGGER = getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


def setup_platform(
    hass: HomeAssistant,
    *_,
    **__,
):
    LOGGER.warn("Here")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    try:
        await account.async_ensure_tokens_valid()
    except ClientError as exc:
        raise ConfigEntryNotReady from exc

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
