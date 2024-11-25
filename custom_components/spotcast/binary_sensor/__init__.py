"""Platform for binary sensor integration.

Functions:
    - async_setup_entry
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.binary_sensor\
    .spotify_profile_malfunction_sensor import (
        SpotifyProfileMalfunctionBinarySensor,
    )
from custom_components.spotcast.binary_sensor.is_default_binary_sensor import (
    IsDefaultBinarySensor,
)

LOGGER = getLogger(__name__)

BINARY_SENSORS = (
    IsDefaultBinarySensor,
    SpotifyProfileMalfunctionBinarySensor,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup for the binaries sensors for a spotcast entry

    Args:
        - hass(HomeAssistant): The Home Assistant Instance
        - entry(ConfigEntry): The config entry being setup
        - async_add_entities(AddEntitiesCallback): The function
            callback for creating binary_sensors
    """

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    built_sensors = []

    for sensor in BINARY_SENSORS:
        LOGGER.debug(
            "Creating Sensor %s for `%s`",
            sensor.GENERIC_NAME,
            account.id
        )

        built_sensors.append(sensor(account))

    async_add_entities(built_sensors, True)
