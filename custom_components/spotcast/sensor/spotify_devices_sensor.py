"""Module for the SpotifyDevicesSensor

Classes:
    - SpotifyDevicesSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import (
    SensorStateClass,
)
from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor

LOGGER = getLogger(__name__)


class SpotifyDevicesSensor(SpotcastSensor):
    """A Home Assistant sensor reporting available devices for a
    Spotify Account

    Attributes:
        - account: The spotify account linked to the sensor

    Properties:
        - units_of_measurement(str): the units of mesaurements used
        - unique_id(str): A unique id for the specific sensor
        - name(str): The friendly name of the sensor
        - state(str): The current state of the sensor
        - state_class(str): The type of state provided by the sensor

    Constants:
        - CLASS_NAME(str): The generic name for the class

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Devices"
    ICON = "mdi:speaker"
    DEFAULT_ATTRIBUTES = {"devices": []}
    UNITS_OF_MEASURE = "devices"

    @property
    def state_class(self) -> str:
        return SensorStateClass.MEASUREMENT

    async def async_update(self):
        try:
            devices = await self.account.async_devices()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            self._attributes["devices"] = []
            return

        LOGGER.debug(
            "Getting Spotify Device for account %s",
            self.account.name
        )

        device_count = len(devices)

        LOGGER.debug(
            "Found %d devices linked to spotify account %s",
            device_count,
            self.account.name
        )

        self._attr_state = device_count
        self._attributes["devices"] = devices
