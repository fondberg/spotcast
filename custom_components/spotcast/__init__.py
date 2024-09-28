from logging import getLogger
from aiohttp import ClientError
from asyncio import sleep

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.spotify.exceptions import TokenError
from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast,
)

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
)


DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    LOGGER.debug(entry)

    return True
