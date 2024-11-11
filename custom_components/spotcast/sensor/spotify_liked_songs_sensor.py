"""The SpotifyLikedSongsSensor object

Classes:
    - SpotifyLikedSongsSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor,
    SensorStateClass,
)

LOGGER = getLogger(__name__)


class SpotifyLikedSongsSensor(SpotcastSensor):
    """A Home Assistant sensor reporting the number of liked songs for
    an account

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

    GENERIC_NAME = "Spotify Liked Songs"
    ICON = "mdi:music-note"
    UNITS_OF_MEASURE = "songs"

    @property
    def state_class(self) -> str:
        return SensorStateClass.MEASUREMENT

    async def async_update(self):

        try:
            liked_songs = await self.account.async_liked_songs()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Getting Spotify Liked Songs for account `%s`",
            self.account.name
        )

        song_count = len(liked_songs)

        LOGGER.debug(
            "Found %d liked songs for spotify account `%s`",
            song_count,
            self.account.name
        )

        self._attr_state = song_count
