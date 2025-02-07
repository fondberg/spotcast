"""Module for the SpotifyDevicesSensor

Classes:
    - SpotifyDevicesSensor
"""

from logging import getLogger

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor

LOGGER = getLogger(__name__)


class SpotifyDevicesSensor(SpotcastSensor):
    """A Home Assistant sensor reporting available devices for a
    Spotify Account

    Properties:
        - state_class(self): the state class of the sensor

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Devices"
    ICON = "mdi:speaker"
    UNITS_OF_MEASURE = "devices"

    @property
    def _default_attributes(self) -> dict:
        """Builds a set of default attributes for the sensor"""
        return {
            "devices": []
        }

    async def _async_update_process(self):
        """Updates the available devices asynchronously"""
        devices = await self.account.async_devices()

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
