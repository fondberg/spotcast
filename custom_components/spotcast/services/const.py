"""Module with constants for service definitions"""

from types import MappingProxyType

from custom_components.spotcast.services.play_media import (
    PLAY_MEDIA_SCHEMA,
    async_play_media,
)
from custom_components.spotcast.services.play_dj import (
    PLAY_DJ_SCHEMA,
    async_play_dj,
)

SERVICE_SCHEMAS = MappingProxyType({
    "play_media": PLAY_MEDIA_SCHEMA,
    "play_dj": PLAY_DJ_SCHEMA,
})

SERVICE_HANDLERS = MappingProxyType({
    "play_media": async_play_media,
    "play_dj": async_play_dj,
})
