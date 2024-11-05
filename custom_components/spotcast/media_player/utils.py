"""Module with utility functions for media_players

Functions:
    - async_entity_from_id
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_get_platforms, Entity
from homeassistant.components.cast.media_player import CastDevice
from homeassistant.components.cast.helpers import ChromeCastZeroconf

from custom_components.spotcast.media_player.exceptions import (
    MediaPlayerNotFoundError,
    UnknownIntegrationError,
)
from custom_components.spotcast.media_player import (
    MediaPlayer,
    Chromecast,
    SpotifyDevice,
)

LOGGER = getLogger(__name__)

PLAYER_TYPES = (
    Chromecast,
    SpotifyDevice,
)


async def async_media_player_from_id(
    hass: HomeAssistant,
    entity_id: str,
) -> MediaPlayer:
    """Retrives an entity from the entity_id"""

    for player_type in PLAYER_TYPES:

        integration = player_type.INTEGRATION

        platforms = async_get_platforms(hass, integration)
        entities = {}

        for platform in platforms:
            if platform.domain == "media_player":
                LOGGER.debug(
                    "Adding %d entities from platform `%s` to prefiltered "
                    "list",
                    len(platform.entities),
                    platform.platform_name,
                )
                entities |= platform.entities

        entity = entities.get(entity_id)

        if entity is None:
            LOGGER.debug(
                "Entity `%s` was not found in integration `%s`",
                entity_id,
                integration,
            )
            continue

        return build_from_integration(entity, integration)

    raise MediaPlayerNotFoundError(
        f"Could not find `{entity_id}` in the managed integrations",
    )


def build_from_integration(entity: Entity, integration: str) -> MediaPlayer:
    """Builds the proper media player based on the integration

    Args:
        - entity(Entity): the entity with the proper id
        - integration(str): name of the integration of the entity

    Returns:
        - MediaPlayer: an object of type media player
    """

    if integration == "cast":

        entity: CastDevice

        return Chromecast(
            entity._cast_info.cast_info,
            zconf=ChromeCastZeroconf.get_zeroconf()
        )

    if integration == "spotcast":
        return entity

    raise UnknownIntegrationError(
        f"The integration `{integration}` is not manageable by spotcast"
    )
