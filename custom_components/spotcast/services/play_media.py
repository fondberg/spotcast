"""Module for the play media service

Functions:
    - async_play_media
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.media_player import Chromecast
from custom_components.spotcast.chromecast import SpotifyController
from custom_components.spotcast.utils import async_get_account_entry
from custom_components.spotcast.services.exceptions import (
    TooManyMediaPlayersError
)

LOGGER = getLogger(__name__)

PLAY_MEDIA_SCHEMA = vol.Schema({
    vol.Required("media_player"): cv.ENTITY_SERVICE_FIELDS,
    vol.Required("spotify_uri"): cv.string,
    vol.Optional("account"): cv.string,
    vol.Optional("data"): dict,
})


async def async_play_media(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    uri: str = call.data.get("spotify_uri")
    account_id: str = call.data.get("account")
    entity_id: dict[str, list] = call.data.get("media_player")
    extra: dict[str] = call.data.get("data")

    entity_count = sum([len(x) for x in entity_id.values()])

    if entity_count != 1:
        raise TooManyMediaPlayersError(
            f"Spotcast can only handle 1 device at a time, {entity_count} "
            "where provided"
        )

    entry = await async_get_account_entry(hass, account_id)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    LOGGER.debug("Getting %s from home assistant", entity_id)
    media_player = Chromecast.from_hass(hass, entity_id["entity_id"][0])
    spotify_controller = SpotifyController(account)
    media_player.register_handler(spotify_controller)

    await hass.async_add_executor_job(
        spotify_controller.launch_app,
        media_player,
    )

    await account.async_play_media(media_player.id, uri)
