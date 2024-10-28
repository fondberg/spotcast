"""The SpotifyPlaylistsSensor object"""

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

        LOGGER.debug(
            "Loading Spotify Playlists sensor for %s",
            self.account.name
        )

        self._id = f"{self.account.id}_playlists"
        self._attr_unique_id = f"{self.account.id}_playlists"
        self._attributes = {"playlists": [], "last_update": None}
        self._attr_device_info = device_from_account(self.account)

        self._playlists = []
        self._attr_state = STATE_UNKNOWN

    @property
    def unit_of_measurement(self) -> str:
        return "playlists"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Playlists"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def state_class(self) -> str:
        return "measurement"

    def async_update(self):
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
        self._attributes["playlists"] = playlists
        self._attributes["last_update"] = dt.datetime.now().isoformat("T")
