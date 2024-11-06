"""Module with utility functions for media_players

Functions:
    - async_entity_from_id
    - async_entities_from_integration
    - async_build_from_integration
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
    SpotifyAccount,
)

from custom_components.spotcast.chromecast import SpotifyController

LOGGER = getLogger(__name__)

PLAYER_TYPES = (
    Chromecast,
    SpotifyDevice,
)


async def async_media_player_from_id(
    hass: HomeAssistant,
    account: SpotifyAccount,
    entity_id: str,
) -> MediaPlayer:
    """Retrives an entity from the entity_id"""

    for player_type in PLAYER_TYPES:

        integration = player_type.INTEGRATION

        entities = await async_entities_from_integration(
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

        return await async_build_from_type(hass, entity, account)

    raise MediaPlayerNotFoundError(
        f"Could not find `{entity_id}` in the managed integrations",
    )


async def async_entities_from_integration(
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


async def async_build_from_type(
        hass: HomeAssistant,
        entity: Entity,
        account: SpotifyAccount
) -> MediaPlayer:
    """Builds the proper media player based on its entity type

    Args:
        - entity(Entity): the entity with the proper id

    Returns:
        - MediaPlayer: an object of type media player
    """

    LOGGER.debug("Building Device of type `%s`", type(Entity))

    if isinstance(entity, CastDevice):
        entity: CastDevice
        media_player = Chromecast(
            entity._cast_info.cast_info,
            zconf=ChromeCastZeroconf.get_zeroconf()
        )

        spotify_controller = SpotifyController(account)
        media_player.register_handler(spotify_controller)

        await hass.async_add_executor_job(
            spotify_controller.launch_app,
            media_player,
        )

        return media_player

    if isinstance(entity, SpotifyDevice):
        return entity

    raise UnknownIntegrationError(
        f"No constructor available for entity of type {type(entity)}"
    )
