"""The SpotifyLikedSongsSensor object

Classes:
    - SpotifyLikedSongsSensor
"""

from logging import getLogger

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor

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

    async def _async_update_process(self):
        """Updates the number of liked songs asynchronously"""

        count = await self.account.async_liked_songs_count()

        LOGGER.debug(
            "Found %d liked songs for spotify account `%s`",
            count,
            self.account.name
        )

        self._attr_state = count
