from __future__ import annotations

import logging

from homeassistant.components import spotify as ha_spotify
from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import MEDIA_CLASS_APP
import homeassistant.core as ha_core
from pychromecast import Chromecast

_LOGGER = logging.getLogger(__name__)


async def async_get_media_browser_root_object(
    hass: ha_core.HomeAssistant,
    cast_type: str
) -> list[BrowseMedia]:
    """Create a root object for media browsing."""
    _LOGGER.debug("async_get_media_browser_root_object")
    return [
        BrowseMedia(
            title="Spotify",
            media_class=MEDIA_CLASS_APP,
            media_content_id="",
            media_content_type="spotify",
            thumbnail="https://brands.home-assistant.io/_/spotify/logo.png",
            can_play=False,
            can_expand=True,
        )
    ]


async def async_browse_media(
    hass: ha_core.HomeAssistant,
    media_content_type: str,
    media_content_id: str,
    cast_type: str,
) -> BrowseMedia | None:
    """Browse media."""
    _LOGGER.debug(
        "async_browse_media %s, %s",
        media_content_type,
        media_content_id
    )
    result = None
    # Check if this media is handled by Spotify, if it isn't just return None.
    if ha_spotify.is_spotify_media_type(media_content_type):
        # Browse deeper in the tree
        result = await ha_spotify.async_browse_media(
            hass, media_content_type, media_content_id, can_play_artist=False
        )
    if media_content_type == "spotify":
        # Browse the root node created by async_get_media_browser_root_object
        result = await ha_spotify.async_browse_media(
            hass, None, None, can_play_artist=False
        )
    _LOGGER.debug(
        "async_browse_media return: %s",
        result
    )
    return result


async def async_play_media(
    hass: ha_core.HomeAssistant,
    cast_entity_id,
    chromecast: Chromecast,
    media_type: str,
    media_id: str,
) -> bool:
    """Play media."""
    _LOGGER.debug(
        "async_browse_media %s, %s",
        media_type,
        media_id
    )
    # If this is a spotify URI, forward to the the spotcast.start service, if not return
    # False
    if media_id and media_id.startswith("spotify:"):
        data = {"entity_id": cast_entity_id, "uri": media_id}
        await hass.services.async_call("spotcast", "start", data, blocking=False)
        return True
    return False
