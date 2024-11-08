"""Module for the play media service

Functions:
    - async_play_media
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry
from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
)

from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
    entity_from_target_selector
)

LOGGER = getLogger(__name__)

PLAY_MEDIA_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("spotify_uri"): cv.string,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_media(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    uri: str = call.data.get("spotify_uri")
    account_id: str = call.data.get("account")
    media_players: dict[str, list] = call.data.get("media_player")
    extras: dict[str] = call.data.get("data")

    if extras is None:
        extras = {}

    entry = get_account_entry(hass, account_id)
    entity_id = entity_from_target_selector(hass, media_players)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    LOGGER.debug("Getting %s from home assistant", entity_id)
    media_player = await async_media_player_from_id(hass, account, entity_id)

    LOGGER.info(
        "Playing `%s` on `%s` for account `%s`",
        uri,
        media_player.name,
        account.id
    )

    await account.async_play_media(media_player.id, uri, **extras)
    await account.async_apply_extras(media_player.id, extras)
