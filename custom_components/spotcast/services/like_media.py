"""Module to like a (list) of spotify uris

Functions:
    - async_like_media
"""

from logging import getLogger

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.utils import url_to_uri

LOGGER = getLogger(__name__)

LIKE_MEDIA_SCHEMA = vol.Schema({
    vol.Required("spotify_uris"): vol.All(cv.ensure_list, [url_to_uri]),
    vol.Optional("account"): cv.string,
})


async def async_like_media(hass: HomeAssistant, call: ServiceCall):
    """Service to add like a (list) of spotify uris"""
    uris = call.data.get("spotify_uris")
    account_id = call.data.get("account")

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    await account.async_like_media(uris)
