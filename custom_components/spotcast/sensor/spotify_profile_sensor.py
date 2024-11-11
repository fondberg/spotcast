"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN, STATE_OK
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor
)

LOGGER = getLogger(__name__)


class SpotifyProfileSensor(SpotcastSensor):
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

    GENERIC_NAME = "Spotify Profile"
    ICON = "mdi:account"
    DEFAULT_ATTRIBUTES = {}

    @property
    def entity_picture(self) -> str:
        if self.state == STATE_OK:
            return self.account.image_link

        return None

    async def async_update(self):
        try:
            profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            self._attributes = {}
            return

        LOGGER.debug(
            "Getting Spotify Profile for account `%s`",
            self.account.name
        )

        LOGGER.debug(
            "Profile retrieve for account id `%s`", profile["id"],
        )

        self._attributes = profile
        self._attr_state = STATE_OK

    @staticmethod
    def _clean_profile(profile: dict) -> dict:
        """Cleans the profile for a better attributes result in Home
        Assistant

        Args:
            - profile(dict): the raw profile from Spotify API

        Returns:
            - dict:a clean profile for better """
