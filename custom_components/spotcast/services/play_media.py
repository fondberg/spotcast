"""Module for the play media service

Functions:
    - async_play_media
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.const import CONF_ENTITY_ID
import voluptuous as vol


from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.media_players import Chromecast
from custom_components.spotcast.chromecast import SpotifyController
from custom_components.spotcast.utils import get_account_entry

LOGGER = getLogger(__name__)

PLAY_MEDIA_SCHEMA = vol.Schema({
    vol.Required(CONF_ENTITY_ID): cv.string,
    vol.Required("account"): cv.string,
    vol.Required("spotify_uri"): cv.string,
})


async def async_play_media(hass: HomeAssistant, call: ServiceCall):
    """Service to start playing media

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - call(ServiceCall): the service call data pack
    """

    uri = call.data.get("spotify_uri")
    account_id = call.data.get("account")
    entity_id = call.data.get("entity_id")

    entry = get_account_entry(hass, account_id)

    LOGGER.debug("Loading Spotify Account for User `%s`", account_id)
    account = await SpotifyAccount.async_from_config_entry(
        hass=hass,
        entry=entry
    )

    LOGGER.debug("Getting %s from home assistant", entity_id)
    media_player = Chromecast.from_hass(hass, entity_id)
    spotify_controller = SpotifyController(account)
    media_player.register_handler(spotify_controller)

    await hass.async_add_executor_job(
        spotify_controller.launch_app,
        media_player,
    )

    await account.async_play_media(media_player.id, uri)
