"""Module for the abstract SpotcastSensor class"""

from logging import getLogger

from homeassistant.const import STATE_UNKNOWN
from homeassistant.components.binary_sensor import BinarySensorEntity

from custom_components.spotcast.sensor.abstract_entity import SpotcastEntity

LOGGER = getLogger(__name__)


class SpotcastBinarySensor(SpotcastEntity, BinarySensorEntity):
    """A generic abstract Spotcast sensor for Home Assistant. can be
    customized through its list of constants for the class

    Properties:
        - is_on(str): Indicate the state of the binary sensor
        - icon(str): the icon to used for the binary sensor. Based on
            the is on state
    """

    PLATFORM = "binary_sensor"

    @property
    def is_on(self) -> str:
        if self._attr_state == STATE_UNKNOWN:
            return None

        return self._attr_state != self.INACTIVE_STATE

    @property
    def icon(self) -> str:
        """Sets the icon of the entity"""

        if self._attr_state == STATE_UNKNOWN or self.is_on:
            return self.ICON

        return self._icon_off
