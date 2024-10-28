"""Module for the SpotifyDevicesSensor"""

from logging import getLogger
from asyncio import run_coroutine_threadsafe
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.utils import device_from_account

LOGGER = getLogger(__name__)


class SpotifyDevicesSensor(SensorEntity):

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, hass: HomeAssistant, account: SpotifyAccount):
        self.account = account

        LOGGER.debug("Loading Spotify Device sensor for %s", self.account.name)

        self._id = f"{self.account.id}_devices"
        self._attr_unique_id = f"{self.account.id}_devices"
        self._attributes = {"devices": [], "last_update": None}
        self._attr_device_info = device_from_account(self.account)

        self._devices = []
        self._attr_state = STATE_UNKNOWN

    @property
    def unit_of_mesaurement(self) -> str:
        return "devices"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Devices"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def extra_state_attributes(self) -> dict:
        return self._attributes

    @property
    def state_class(self) -> str:
        return "measurement"

    def update(self):
        LOGGER.debug(
            "Getting Spotify Device for account %s",
            self.account.name
        )

        devices = run_coroutine_threadsafe(
            self.account.async_devices(),
            self.hass.loop
        ).result()

        device_count = len(devices)

        LOGGER.debug(
            "Found %d devices linked to spotify account %s",
            device_count,
            self.account.name
        )

        self._attr_state = device_count
        self._attributes["devices"] = devices
        self._attributes["last_update"] = dt.datetime.now().isoformat("T")
