from logging import getLogger
from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.spotify.exceptions import TokenError


DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    implementation = await async_get_config_entry_implementation(hass, entry)
    session = OAuth2Session(hass, entry, implementation)

    try:
        await session.async_ensure_token_valid()
    except ClientError as exc:
        raise ConfigEntryNotReady from exc

    try:
        account = SpotifyAccount.from_oauth_session(session)
    except TokenError as exc:
        raise ConfigEntryNotReady from exc

    LOGGER.debug(await account.async_connect())

    return True
