"""Module for the play custom context

Functions:
    - async_play_custom_context
"""

from logging import getLogger
from random import randint

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.exceptions import ServiceValidationError
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry
from custom_components.spotcast.spotify.utils import url_to_uri
from custom_components.spotcast.media_player.utils import (
    async_media_player_from_id,
    MissingActiveDeviceError,
)

from custom_components.spotcast.services.utils import (
    EXTRAS_SCHEMA,
    entity_from_target_selector
)

LOGGER = getLogger(__name__)

PLAY_CUSTOM_CONTEXT_SCHEMA = vol.Schema({
    vol.Optional("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("tracks"): vol.All(cv.ensure_list, [url_to_uri]),
    vol.Optional("account"): cv.string,
    vol.Optional("data"): EXTRAS_SCHEMA,
})


async def async_play_custom_context(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    tracks: list[str] = call.data.get("tracks")
    account_id: str = call.data.get("account")
    media_players: dict[str, list] = call.data.get("media_player")
    extras: dict[str] = call.data.get("data", {})

    entry = get_account_entry(hass, account_id)
    entity_id = None

    if media_players is not None:
        entity_id = entity_from_target_selector(hass, media_players)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    if entity_id is not None:
        LOGGER.debug("Getting %s from home assistant", entity_id)
    else:
        LOGGER.debug("Getting active device for account `%s`", account.name)

    try:
        media_player = await async_media_player_from_id(
            hass,
            account,
            entity_id,
        )
    except MissingActiveDeviceError as exc:
        raise ServiceValidationError(str(exc)) from exc

    LOGGER.info(
        "Playing %d items in custom context for accout `%s`",
        len(tracks),
        account.id,
    )

    if extras.get("random", False):
        extras["offset"] = randint(0, len(tracks)-1)

    await account.async_play_media(media_player.id, uris=tracks, **extras)
    await account.async_apply_extras(media_player.id, extras)
