"""Platform for sensor integration."""

from logging import getLogger
from asyncio import run_coroutine_threadsafe
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType
from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast import (
    SpotifyAccount,
    DOMAIN,
)

LOGGER = getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    LOGGER.debug(entry)

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    async_add_entities([SpotifyDevicesSensor(hass, account)], True)


class SpotifyDevicesSensor(SensorEntity):

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, hass: HomeAssistant, account: SpotifyAccount):
        self.account = account
        profile = self.account.profile
        LOGGER.warn(profile)

        LOGGER.debug("Loading Spotify Device sensor for %s", self.account.name)

        self._id = f"{self.account.id}_devices"
        self._attr_unique_id = f"{self.account.id}_devices"
        self._attributes = {"devices": [], "last_update": None}

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.account.id)},
            manufacturer="Spotify AB",
            model=f"Spotify {profile['product']}",
            name=f"Spotcast {account.name}",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://open.spotify.com",
        )

        self._devices = []
        self._attr_state = STATE_UNKNOWN

    @property
    def name(self):
        return f"{self.account.name} Spotify Devices"

    @property
    def state(self):
        return self._attr_state

    @property
    def extra_state_attributes(self):
        return self._attributes

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
