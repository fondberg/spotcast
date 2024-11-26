"""Platform for sensor integration.

Functions:
    - async_setup_entry
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.sensor.spotify_devices_sensor import (
    SpotifyDevicesSensor,
)
from custom_components.spotcast.sensor.spotify_playlists_sensor import (
    SpotifyPlaylistsSensor,
)
from custom_components.spotcast.sensor.spotify_profile_sensor import (
    SpotifyProfileSensor,
)
from custom_components.spotcast.sensor.spotify_liked_songs_sensor import (
    SpotifyLikedSongsSensor
)
from custom_components.spotcast.sensor.spotify_product_sensor import (
    SpotifyProductSensor
)
from custom_components.spotcast.sensor.spotify_followers_sensor import (
    SpotifyFollowersSensor
)
from custom_components.spotcast.sensor.spotify_account_type_sensor import (
    SpotifyAccountTypeSensor
)

LOGGER = getLogger(__name__)
SENSORS = (
    SpotifyDevicesSensor,
    SpotifyPlaylistsSensor,
    SpotifyProfileSensor,
    SpotifyLikedSongsSensor,
    SpotifyProductSensor,
    SpotifyFollowersSensor,
    SpotifyAccountTypeSensor,
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
            sensor.GENERIC_NAME,
            account.id
        )

        built_sensors.append(sensor(account))

    async_add_entities(built_sensors, True)
