"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    EntityCategory,
)
from homeassistant.const import STATE_UNKNOWN, STATE_OK
from requests.exceptions import ReadTimeout

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotifyProfileSensor(SensorEntity):
    """A Home Assistant sensor reporting information about the profile
    of a Spotify Account

    Attributes:
        - account: The spotify account linked to the sensor

    Properties:
        - units_of_measurement(str): the units of mesaurements used
        - unique_id(str): A unique id for the specific sensor
        - name(str): The friendly name of the sensor
        - state(str): The current state of the sensor

    Constants:
        - CLASS_NAME(str): The generic name for the class

    Methods:
        - async_update
    """

    CLASS_NAME = "Spotify Profile Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting the profile for a
        Spotify Account

        Args:
            - account(SpotifyAccount): The spotify account probed by
                the sensor
        """
        self.account = account

        LOGGER.debug(
            "Loading Spotify Playlists sensor for %s",
            self.account.name
        )

        self._attributes = {}
        self._attr_device_info = self.account.device_info

        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_profile"

    @property
    def icon(self) -> str:
        return "mdi:account"

    @property
    def entity_picture(self) -> str:
        if self.state == STATE_OK:
            return self.account.image_link

        return None

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
            "Getting Spotify Profile for account `%s`",
            self.account.name
        )

        try:
            self._profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            self._attributes = {}
            return

        LOGGER.debug(
            "Profile retrieve for account id `%s`", self._profile["id"],
        )

        self._attributes = self._profile
        self._attr_state = STATE_OK

    @staticmethod
    def _clean_profile(profile: dict) -> dict:
        """Cleans the profile for a better attributes result in Home
        Assistant

        Args:
            - profile(dict): the raw profile from Spotify API

        Returns:
            - dict:a clean profile for better """
