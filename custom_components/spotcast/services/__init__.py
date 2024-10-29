"""Module for all the spotcast services"""

from types import MappingProxyType

from custom_components.spotcast.services.service_handler import (
    ServiceHandler
)

from custom_components.spotcast.services.play_media import PLAY_MEDIA_SCHEMA

SERVICE_SCHEMAS = MappingProxyType({
    "play_media": PLAY_MEDIA_SCHEMA
})
