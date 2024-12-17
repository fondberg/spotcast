"""The SpotifyLikedSongsSensor object

Classes:
    - SpotifyLikedSongsSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor
from custom_components.spotcast.sessions.exceptions import (
    UpstreamServerNotready,
)

LOGGER = getLogger(__name__)


class SpotifyLikedSongsSensor(SpotcastSensor):
    """A Home Assistant sensor reporting the number of liked songs for
    an account

    properties:
        - state_class(str): the state class of the sensor

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Liked Songs"
    ICON = "mdi:music-note"
    UNITS_OF_MEASURE = "songs"

    async def async_update(self):
        """Updates the number of liked songs asynchronously"""

        try:
            count = await self.account.async_liked_songs_count()
        except (ReadTimeoutError, ReadTimeout, UpstreamServerNotready):
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Found %d liked songs for spotify account `%s`",
            count,
            self.account.name
        )

        self._attr_state = count
