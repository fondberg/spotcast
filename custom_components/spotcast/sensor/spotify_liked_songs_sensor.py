"""The SpotifyLikedSongsSensor object

Classes:
    - SpotifyLikedSongsSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotifyLikedSongsSensor(SensorEntity):
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

    CLASS_NAME = "Spotify Liked Songs Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting liked songs for a
        Spotify Account

        Args:
            - account(SpotifyAccount): The spotify account probed by
                the sensor
        """

        self.account = account

        LOGGER.debug(
            "Loading Spotify Liked Songs sensor for %s",
            self.account.name
        )

        self._attr_device_info = self.account.device_info

        self._playlists = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_liked_songs"

    @property
    def unit_of_measurement(self) -> str:
        return "songs"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Liked Songs"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_liked_songs"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def state_class(self) -> str:
        return "measurement"

    @property
    def icon(self) -> str:
        """Sets the icon for the sensor"""
        return "mdi:music-note"

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify Liked Songs for account `%s`",
            self.account.name
        )

        try:
            liked_songs = await self.account.async_liked_songs()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            return

        song_count = len(liked_songs)

        LOGGER.debug(
            "Found %d liked songs for spotify account `%s`",
            song_count,
            self.account.name
        )

        self._attr_state = song_count
