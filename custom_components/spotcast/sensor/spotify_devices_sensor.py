"""Module for the SpotifyDevicesSensor

Classes:
    - SpotifyDevicesSensor
"""

from logging import getLogger

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.utils import device_from_account

LOGGER = getLogger(__name__)


class SpotifyDevicesSensor(SensorEntity):
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

    CLASS_NAME = "Spotify Devices Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting available devices for a
        Spotify Account

        Args:
            - account(SpotifyAccount): The spotify account the sensor
            is probing
        """

        self.account = account

        LOGGER.debug("Loading Spotify Device sensor for %s", self.account.name)

        self._attributes = {"devices": []}
        self._attr_device_info = device_from_account(self.account)

        self._devices = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_devices"

    @property
    def unit_of_mesaurement(self) -> str:
        return "devices"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_devices"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Devices"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def state_class(self) -> str:
        return "measurement"

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify Device for account %s",
            self.account.name
        )

        devices = await self.account.async_devices(),

        device_count = len(devices)

        LOGGER.debug(
            "Found %d devices linked to spotify account %s",
            device_count,
            self.account.name
        )

        self._attr_state = device_count
        self._attributes["devices"] = devices
