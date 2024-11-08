"""The SpotifyFollowersSensor object

Classes:
    - SpotifyFollowersSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.utils import device_from_account

LOGGER = getLogger(__name__)


class SpotifyFollowersSensor(SensorEntity):
    """A Home Assistant sensor reporting the number of followers for
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

    CLASS_NAME = "Spotify Followers Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting followers for a
        Spotify Account

        Args:
            - account(SpotifyAccount): The spotify account probed by
                the sensor
        """

        self.account = account

        LOGGER.debug(
            "Loading Spotify Followers sensor for %s",
            self.account.name
        )

        self._attr_device_info = device_from_account(self.account)

        self._playlists = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_followers"
        self._profile = {}

    @property
    def unit_of_measurement(self) -> str:
        return "followers"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Followers"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_followers"

    @property
    def state(self) -> str:
        return self._attr_state

    @property
    def state_class(self) -> str:
        return "measurement"

    @property
    def icon(self) -> str:
        """Sets the icon for the sensor"""
        return "mdi:account-multiple"

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify followers for account `%s`",
            self.account.name
        )

        try:
            self._profile = await self.account.async_profile()
        except ReadTimeoutError:
            self._attr_state = STATE_UNKNOWN
            return

        follower_count = self._profile["followers"]["total"]

        LOGGER.debug(
            "Found %d followers for spotify account `%s`",
            follower_count,
            self.account.name
        )

        self._attr_state = follower_count
