"""The SpotifyProfileSensor object"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN, STATE_OK

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.utils import device_from_account

LOGGER = getLogger(__name__)


class SpotifyProfileSensor(SensorEntity):

    CLASS_NAME = "Spotify Profile Sensor"

    def __init__(self, hass: HomeAssistant, account: SpotifyAccount):
        self.account = account

        LOGGER.debug(
            "Loading Spotify Playlists sensor for %s",
            self.account.name
        )

        self._attributes = {}
        self._attr_device_info = device_from_account(self.account)

        self._playlists = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_profile"

    @property
    def extra_state_attributes(self) -> dict:
        return self._attributes

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Profile"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_profile"

    @property
    def state(self) -> str:
        return self._attr_state

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify Playlist for account `%s`",
            self.account.name
        )

        profile = await self.account.async_profile()

        LOGGER.debug(
            "Profile retrieve for account id `%s`", profile["id"],
        )

        self._attributes = profile
        self._attr_state = STATE_OK
