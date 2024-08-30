"""Utility functions to interact with chromecast devices

Functions:
    - extract_media_players
"""

from logging import getLogger

from homeassistant.components.cast.media_player import CastDevice
from homeassistant.helpers.entity_platform import EntityPlatform

LOGGER = getLogger(__name__)


def extract_media_players(platform: EntityPlatform) -> dict[str, CastDevice]:
    """Extracts the media_players from a Home Assistant Platform"""

    media_players = {}

    for id, entity in platform.entities.items():

        if not isinstance(entity, CastDevice):
            continue

        LOGGER.debug("Found media player `%s (%s)`", id, entity._name)

        media_players[id] = entity

    return media_players
