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
from custom_components.spotcast.services.play_category import (
    PLAY_CATEGORY_SCHEMA,
    async_play_category,
)
from custom_components.spotcast.services.play_custom_context import (
    PLAY_CUSTOM_CONTEXT_SCHEMA,
    async_play_custom_context,
)
from custom_components.spotcast.services.play_from_search import (
    PLAY_FROM_SEARCH_SCHEMA,
    async_play_from_search,
)
from custom_components.spotcast.services.add_to_queue import (
    ADD_TO_QUEUE_SCHEMA,
    async_add_to_queue,
)

SERVICE_SCHEMAS = MappingProxyType({
    "play_media": PLAY_MEDIA_SCHEMA,
    "play_dj": PLAY_DJ_SCHEMA,
    "play_liked_songs": PLAY_LIKED_SONGS_SCHEMA,
    "transfer_playback": TRANSFER_PLAYBACK_SCHEMA,
    "play_category": PLAY_CATEGORY_SCHEMA,
    "play_custom_context": PLAY_CUSTOM_CONTEXT_SCHEMA,
    "play_from_search": PLAY_FROM_SEARCH_SCHEMA,
    "add_to_queue": ADD_TO_QUEUE_SCHEMA,
})

SERVICE_HANDLERS = MappingProxyType({
    "play_media": async_play_media,
    "play_dj": async_play_dj,
    "play_liked_songs": async_play_liked_songs,
    "transfer_playback": async_transfer_playback,
    "play_category": async_play_category,
    "play_custom_context": async_play_custom_context,
    "play_from_search": async_play_from_search,
    "add_to_queue": async_add_to_queue,
})
