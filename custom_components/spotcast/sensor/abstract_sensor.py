"""Module for the abstract SpotcastSensor class"""

from logging import getLogger

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
    EntityCategory,
)

from custom_components.spotcast.sensor.abstract_entity import SpotcastEntity

LOGGER = getLogger(__name__)


class SpotcastSensor(SpotcastEntity):
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

    PLATFORM = "sensor"
    UNITS_OF_MEASURE: str = None

    @property
    def units_of_measurement(self) -> str:
        """Returns the units measured by the sensor"""
        return self.UNITS_OF_MEASURE

    @property
    def state(self) -> str | int | float:
        """Returns the currently saved state of the sensor"""
        return self._attr_state

    @property
    def icon(self) -> str:
        """Sets the icon of the entity"""

        state = self._attr_state
        if (
            isinstance(state, str) and state != self.INACTIVE_STATE
            or isinstance(state, int) and state > 0
        ):
            return self.ICON

        return self._icon_off
