"""The SpotifyPlaylistsSensor object"""

from logging import getLogger
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.utils import device_from_account

LOGGER = getLogger(__name__)


class SpotifyPlaylistsSensor(SensorEntity):

    CLASS_NAME = "Spotify Playlists Sensor"

    def __init__(self, hass: HomeAssistant, account: SpotifyAccount):
        self.account = account

        LOGGER.debug(
            "Loading Spotify Playlists sensor for %s",
            self.account.name
        )

        self._attributes = {"playlists": [], "last_update": None}
        self._attr_device_info = device_from_account(self.account)

        self._playlists = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_playlists"

    @property
    def extra_state_attributes(self) -> dict:
        return self._attributes

    @property
    def unit_of_measurement(self) -> str:
        return "playlists"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Playlists"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_playlists"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def state_class(self) -> str:
        return "measurement"

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify Playlist for account `%s`",
            self.account.name
        )

        playlists = await self.account.async_playlists()

        playlist_count = len(playlists)

        LOGGER.debug(
            "Found %d playlist for spotify account `%s`",
            playlist_count,
            self.account.name
        )

        self._attr_state = playlist_count
        self._attributes["first_10_playlists"] = playlists[:10]
        self._attributes["last_update"] = dt.datetime.now().isoformat("T")