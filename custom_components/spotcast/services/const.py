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
from custom_components.spotcast.services.play_liked_songs import (
    PLAY_LIKED_SONGS_SCHEMA,
    async_play_liked_songs,
)
from custom_components.spotcast.services.transfer_playback import (
    TRANSFER_PLAYBACK_SCHEMA,
    async_transfer_playback,
)

SERVICE_SCHEMAS = MappingProxyType({
    "play_media": PLAY_MEDIA_SCHEMA,
    "play_dj": PLAY_DJ_SCHEMA,
    "play_liked_songs": PLAY_LIKED_SONGS_SCHEMA,
    "transfer_playback": TRANSFER_PLAYBACK_SCHEMA,
})

SERVICE_HANDLERS = MappingProxyType({
    "play_media": async_play_media,
    "play_dj": async_play_dj,
    "play_liked_songs": async_play_liked_songs,
    "transfer_playback": async_transfer_playback,
})
