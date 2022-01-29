from collections.abc import Callable

from homeassistant.components import spotify as ha_spotify
from homeassistant.components.media_player import BrowseMedia
from homeassistant.components.media_player.const import MEDIA_CLASS_APP
import homeassistant.core as ha_core
from pychromecast import Chromecast


async def async_get_media_browser_root_object(
    content_filter: Callable[[BrowseMedia], bool]
):
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
    content_filter: Callable[[BrowseMedia], bool],
):
    if ha_spotify.is_spotify_media_type(media_content_type):
        return await ha_spotify.async_browse_media(
            hass, media_content_type, media_content_id, can_play_artist=False
        )
    if media_content_type == "spotify":
        return await ha_spotify.async_browse_media(
            hass, None, None, can_play_artist=False
        )
    return None


async def async_play_media(
    hass: ha_core.HomeAssistant,
    cast_entity_id,
    chromecast: Chromecast,
    media_type: str,
    media_id: str,
):
    if media_id and media_id.startswith("spotify:"):
        data = {"entity_id": cast_entity_id, "uri": media_id}
        await hass.services.async_call("spotcast", "start", data, blocking=False)
        return True
    return False
