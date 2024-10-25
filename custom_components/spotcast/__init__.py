from logging import getLogger
from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
    async_get_config_entry_implementation,
)

from custom_components.spotcast.spotify import SpotifyAccount


DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    implementation = await async_get_config_entry_implementation(hass, entry)
    country = entry.data.get("country")

    account = SpotifyAccount(
        external_session=OAuth2Session(hass, entry, implementation),
        internal_session=InternalSession(hass, **entry.data["internal_api"]),
        country=country,
    )

    try:
        await account.async_ensure_tokens_valid()
    except ClientError as exc:
        raise ConfigEntryNotReady from exc

    return True
