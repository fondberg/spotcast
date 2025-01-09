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
    MissingActiveDeviceError,
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
    entity_id: str = None,
) -> MediaPlayer:
    """Retrives an entity from the entity_id

    Args:
        - hass(HomeAssistant): the Home Assistant instance
        - account(SpotifyAccount): the account linked to the request
        - entity_id(str, optional): the entity_id of the media player
            to retrieve. Defaults to the active device of the account

    Returns:
        - MediaPlayer: the media player linked to the entity id
            provided
    """

    if entity_id is None:
        return await async_active_device(account)

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


async def async_active_device(account: SpotifyAccount) -> SpotifyDevice:
    """Returns the currently active device for the spotify account.
    Raises an error if there are no active playback

    Args:
        - account(SpotifyAccount): the account to look for an active
            device

    Returns:
        - SpotifyDevice: the media player instance of the active
            device

    Raises:
        - MissingActiveDeviceError: raised when no active playback exist
    """
    playback_state = await account.async_playback_state(force=True)

    if playback_state == {}:
        raise MissingActiveDeviceError(
            "No active playback available. A target must be provided"
        )

    media_player = SpotifyDevice(account, playback_state["device"])

    return media_player


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


def need_to_quit_app(
    media_player: Chromecast,
    active_device: str,
    app_id: str = SpotifyController.APP_ID,
) -> bool:
    """Returns True if the CastDevice needs to quit the app its
    currently running before registering Spotify for the account

    Args:
        - media_player(Chromecast): the cast device to check
        - active_device(str): The id of the currently active device
            on the account
        - app_id(str, optional): The spotify App ID. Defaults to the
            app_id set in the SpotifyController

    Returns:
        - bool: True if needs to quit the app
    """

    return (
        (
            media_player.app_id == app_id
            and media_player.id != active_device
        ) or media_player.app_id is not None
    )


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

        await hass.async_add_executor_job(media_player.wait)

        spotify_controller = SpotifyController(account)
        media_player.register_handler(spotify_controller)
        await account.async_playback_state()

        do_quit = need_to_quit_app(media_player, account.active_device)
        running_spotify = media_player.app_id == spotify_controller.APP_ID

        if do_quit:
            media_player.quit_app()

        if not running_spotify or do_quit:
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
