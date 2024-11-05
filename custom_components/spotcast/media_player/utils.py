"""Module with utility functions for media_players

Functions:
    - entity_from_id
    - entities_from_integration
    - build_from_integration
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.entity import Entity
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


def media_player_from_id(
    hass: HomeAssistant,
    entity_id: str,
) -> MediaPlayer:
    """Retrives an entity from the entity_id"""

    for player_type in PLAYER_TYPES:

        integration = player_type.INTEGRATION

        entities = entities_from_integration(
            hass,
            integration,
            ["media_player"],
        )

        entity = entities.get(entity_id)

        if entity is None:
            LOGGER.debug(
                "Entity `%s` was not found in integration `%s`",
                entity_id,
                integration,
            )
            continue

        return build_from_type(entity)

    raise MediaPlayerNotFoundError(
        f"Could not find `{entity_id}` in the managed integrations",
    )


def entities_from_integration(
        hass: HomeAssistant,
        integration: str,
        platform_filter: list[str] = None,
) -> dict[str, Entity]:
    """Retrives entities from an integration with ability to filter
    platforms

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - integration(str): the name of the integration to pull
            entities from.
        - platform_filter(list[str], optional): a list of platforms to
            filter for. Doesn't filter if None. Defaults to None.

    Returns:
        - dict[str, Entity]: a dictionary of entities using the
            entity_id as the key.
    """

    platforms = async_get_platforms(hass, integration)
    entities = {}

    for platform in platforms:
        if platform_filter is None or platform.domain in platform_filter:
            LOGGER.debug(
                "Adding %d entities from platform `%s`",
                len(platform.entities),
                platform.platform_name,
            )
            entities |= platform.entities

    return entities


def build_from_type(entity: Entity) -> MediaPlayer:
    """Builds the proper media player based on its entity type

    Args:
        - entity(Entity): the entity with the proper id

    Returns:
        - MediaPlayer: an object of type media player
    """

    LOGGER.debug("Building Device of type `%s`", type(Entity))

    if isinstance(entity, CastDevice):
        entity: CastDevice
        return Chromecast(
            entity._cast_info.cast_info,
            zconf=ChromeCastZeroconf.get_zeroconf()
        )

    if isinstance(entity, SpotifyDevice):
        return entity

    raise UnknownIntegrationError(
        f"No constructor available for entity of type {type(entity)}"
    )
