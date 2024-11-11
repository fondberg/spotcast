"""The SpotifyPlaylistsSensor object

Classes:
    - SpotifyPlaylistsSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import (
    SensorStateClass,
    SpotcastSensor,
)

LOGGER = getLogger(__name__)


class SpotifyPlaylistsSensor(SpotcastSensor):
    """A Home Assistant sensor reporting available playlists for a
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

    GENERIC_NAME = "Spotify Playlists"
    ICON = "mdi:playlist-music"
    ICON_OFF = ICON
    DEFAULT_ATTRIBUTES = {"first_10_playlists": []}
    UNITS_OF_MEASURE = "playlists"

    @property
    def state_class(self) -> str:
        return SensorStateClass.MEASUREMENT

    async def async_update(self):

        try:
            playlists = await self.account.async_playlists()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            self._attributes["first_10_playlists"] = []
            return

        LOGGER.debug(
            "Getting Spotify Playlist for account `%s`",
            self.account.name
        )

        playlist_count = len(playlists)

        LOGGER.debug(
            "Found %d playlist for spotify account `%s`",
            playlist_count,
            self.account.name
        )

        self._attr_state = playlist_count
        self._attributes["first_10_playlists"] = playlists[:10]
