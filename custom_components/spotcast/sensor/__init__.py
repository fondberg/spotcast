"""Platform for sensor integration."""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.spotify_devices_sensor import (
    SpotifyDevicesSensor,
)
from custom_components.spotcast.sensor.spotify_playlists_sensor import (
    SpotifyPlaylistsSensor,
)

from custom_components.spotcast.sensor.spotify_profile_sensor import (
    SpotifyProfileSensor,
)

LOGGER = getLogger(__name__)
SENSORS = (
    SpotifyDevicesSensor,
    SpotifyPlaylistsSensor,
    SpotifyProfileSensor,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    built_sensors = []

    for sensor in SENSORS:
        LOGGER.debug(
            "Creating Sensor %s for `%s`",
            sensor.CLASS_NAME,
            account.id
        )

        built_sensors.append(sensor(hass, account))

    async_add_entities(
        built_sensors,
        True
    )
