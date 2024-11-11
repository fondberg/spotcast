"""Module for the abstract SpotcastEntity class"""

from abc import ABC, abstractmethod
from logging import getLogger

from homeassistant.components.sensor import (
    EntityCategory,
    Entity
)
from homeassistant.const import STATE_UNKNOWN, STATE_OFF

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotcastEntity(ABC, Entity):
    """A generic abstract Spotcast sensor for Home Assistant. can be
    customized through its list of constants for the class

    Attributes:
        - account(SpotifyAccount): the spotify account linked to the
            sensor.
        - entity_id(str): The entity_id of the sensor in Home Assistant

    Constants:
        - GENERIC_NAME(str): the generic name of the sensor used in
            Home Assistant frontend
        - GENERIC_ID(str): the generic id to add to the entity id and
            unique id for identification in Home Assistant
        - ICON(str): the mdi icon to use for the entity.
        - ICON_OFF(str, optional): the icon to use for off state. If
            None, uses the `-off` variant of the ICON constant. Defaults
            to None.
        - DEFAULT_ATTRIBUTES(dict[str, str], optional): the default
            extra attributes for the entity. None if the sensor doesn't
            report extra attributes
        - INACTIVE_STATE(str): the state use to signify an OFF state.
            Ignored in the case of numeric state.

    Properties:
        - name(str): the name of the device based on the account name
            and generic_name
        - unique_id(str): the unique_id of the sensor based on the
            account id and generic_id
        - icon(str): the icon to use for the device. Based on ICON
            and ICON_OFF

    Methods:
        - async_update
    """

    GENERIC_NAME: str = "Abstract Spotcast"
    GENERIC_ID: str = None
    PLATFORM: str = None
    DEVICE_SOURCE: str = "account"
    ICON: str = "mdi:cube"
    ICON_OFF: str = None
    DEFAULT_ATTRIBUTES: dict = None
    INACTIVE_STATE: str | int = STATE_OFF
    ENTITY_CATEGORY: str = None

    def __init__(self, account: SpotifyAccount):
        self.account = account

        LOGGER.debug(
            "Loading %s sensor for %s",
            self.GENERIC_NAME,
            self.account.name,
        )

        self._attributes = self.DEFAULT_ATTRIBUTES
        self._attr_state = STATE_UNKNOWN
        self.entity_id = (
            f"{self.PLATFORM}.{self.account.id}_{self._generic_id}"
        )
        self._attr_device_info = self._get_device_info()
        self.entity_category = self.ENTITY_CATEGORY

    def _get_device_info(self):
        if self.DEVICE_SOURCE is None:
            return None

        if self.DEVICE_SOURCE == "account":
            return self.account.device_info

        raise ValueError(f"`{self.DEVICE_SOURCE}` is not a valid source")

    @property
    def _generic_id(self) -> str:
        if self.GENERIC_ID is None:
            id = self.GENERIC_NAME.lower()
            id = id.replace(" ", "_")
            return id

        return self.GENERIC_ID

    @property
    def _icon_off(self) -> str:
        """Returns the icon to show if the entity is inactive
        """

        icon_off = self.ICON_OFF

        if icon_off is None:
            icon_off = f"{self.ICON}-off"

        return icon_off

    @property
    def extra_state_attributes(self) -> dict:
        """Returns the extra attributes of the sensor if exist"""
        return self._attributes

    @property
    def name(self) -> str:
        """returns the name of the entity"""
        return f"{self.account.name} {self.GENERIC_NAME}"

    @property
    def unique_id(self) -> str:
        """returns a unique id for the entity"""
        return f"{self.PLATFORM}.{self.account.id}_{self._generic_id}"

    @property
    @abstractmethod
    def icon(self) -> str:
        """returns the mdi name of the icon to show in Home Assistant
        """

    @abstractmethod
    async def async_update(self):
        """Asynchronous method to update the sensor"""
