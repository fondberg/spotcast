"""Module for the browse media"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.components import spotify as ha_spotify
from homeassistant.components.media_player import BrowseMedia
from pychromecast import Chromecast

from custom_components.spotcast import DOMAIN

LOGGER = getLogger(__name__)


async def async_get_media_browser_root_object(
    hass: HomeAssistant,
    cast_type: str
) -> list:
    """Create a root object for media browsing"""
    result = await ha_spotify.async_browse_media(hass, None, None)
    return result.children


async def async_browse_media(
    hass: HomeAssistant,
    media_content_type: str,
    media_content_id: str,
    cast_type: str,
) -> BrowseMedia | None:
    """Browse media"""
    if not ha_spotify.is_spotify_media_type(media_content_type):
        LOGGER.debug(
            "`%s` is not a valid spotify media type, skipping media browsing",
            media_content_type
        )
        return None

    LOGGER.debug(
        "Browsing for `%s`(%s) - `%s`",
        media_content_id,
        media_content_type,
        cast_type,
    )

    media_browser = await ha_spotify.async_browse_media(
        hass=hass,
        media_content_type=media_content_type,
        media_content_id=media_content_id,
        can_play_artist=False
    )

    return media_browser


async def async_play_media(
    hass: HomeAssistant,
    cast_entity_id: str,
    chromecast: Chromecast,
    media_type: str,
    media_id: str,
) -> bool:
    """Play Media"""
    if media_id is None or not media_id.startswith("spotify:"):
        LOGGER.debug("`%s` is not a valid spotify media id")
        return False

    LOGGER.debug(
        "Starting playback for `%s` on device `%s`(%s)",
        cast_entity_id,
        media_id,
        media_type
    )
    spotify_uri = ha_spotify.spotify_uri_from_media_browser_url(media_id)
    data = {
        "media_player": {
            "entity_id": [
                cast_entity_id
            ]
        },
        "spotify_uri": spotify_uri
    }

    await hass.services.async_call(DOMAIN, "play_media", data, blocking=False)
    return True
