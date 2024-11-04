"""Abstract Media Player class for all iot media player type

Classes:
    - MediaPlayer
"""

from abc import ABC, abstractstaticmethod, abstractmethod
from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_get_platforms

from custom_components.spotcast.media_player.exceptions import (
    InvalidPlatformError,
    MissingDeviceTypeError,
)


LOGGER = getLogger(__name__)


class MediaPlayer(ABC):
    """Abstract Media Player class for all iot media player type

    Constants:
        - DOMAIN(str): the domain of device in HomeAssistant
        - PLATFORM(str): the name of the integration platform in
            HomeAssistant

    Functions:
        - from_hass
        - from_network
    """

    DOMAIN: str = "media_player"
    PLATFORM: str = None
    DEVICE_TYPE: type = None

    @property
    @abstractmethod
    def id(self) -> str:
        """The spotify device id of the player"""

    @abstractstaticmethod
    def from_hass(
        hass: HomeAssistant,
        device_id: str,
        is_device_name: bool = False
    ) -> "MediaPlayer":
        """Imports a Media Player instance from Home Assistant

        Args:
            - hass(HomeAssistant): the home assistant server
            - id(str): the identifier of the device. Can be an entity
                id or a device name. See is_device_name arguments for
                more details.
            - is_device_name(bool, optional): If True, treats the
                device_id as the device name. Otherwise treats it as
                an entity_id. Defaults to False.

        Raises:
            - MediaPlayerNotFoundError: Raised if the player could not
                be found
        """

    @classmethod
    def _get_entities_from_platforms(
            cls,
            hass: HomeAssistant,
            by_device_name: bool = False
    ) -> dict[str]:
        """Returns a dictionary of all media_player entities in
        HomeAssistant that are under the platform of the class.

        Args:
            - hass(HomeAssistant): The HomeAssistant server
            - by_device_name(bool, optional): Keys the devices by
                device name instead of entity_id if True. Defaults to
                False.

        Returns:
            - dict[str]: a dictiomnary where the key is either the
                device name of entity_id (see `by_device_name`). The
                value type will depend on the integration called (See
                value of `DEVICE_TYPE`).

        Raises:
            - InvalidPlatformError: Raised if the requested platform is
                invalid (missing from implementation or inexistant in
                Home Assistant)
            - MissingDeviceTypeError: No Device Type were provided for
                the implementation
        """

        # check if code running from the Abstract Class
        if cls.PLATFORM is None:
            raise InvalidPlatformError(
                "Platform is missing. The child media player is improperly "
                "implemented or you are using the abstract class"
            )

        if cls.DEVICE_TYPE is None:
            raise MissingDeviceTypeError(
                "Device type is missing. The child media player is improperly "
                "implemented or you are using the abstract class"
            )

        # Get all platform fitting the given name
        platforms = async_get_platforms(hass, cls.PLATFORM)
        LOGGER.debug(
            "Retrived platforms: %s",
            str([x.platform_name for x in platforms]),
        )

        # add entities from all domain part of the proper domain
        entities = {}

        for platform in platforms:
            if platform.domain == cls.DOMAIN:
                LOGGER.debug(
                    "Adding %d entites from platform `%s` to prefiltered list",
                    len(platform.entities),
                    platform.platform_name,
                )
                entities |= platform.entities

        # filter the entites for the proper device type
        filtered_entities = {}

        for id, entity in entities.items():

            if not isinstance(entity, cls.DEVICE_TYPE):
                LOGGER.debug(
                    "Removing `%s`. Entity is not of type `%d`",
                    id,
                    str(cls.DEVICE_TYPE)
                )
                continue

            LOGGER.debug("Found device `%s`", id)

            final_id = entity.name if by_device_name else id
            filtered_entities[final_id] = entity

        return filtered_entities

    @abstractstaticmethod
    def from_network() -> "MediaPlayer":
        """Imports a Media Player from the network

        Raises:
            - MediaPlayerNotFoundError: Raised if the player could not
                be found
        """
