"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.binary_sensor import (
    EntityCategory,
)
from homeassistant.const import STATE_OK, STATE_PROBLEM
from requests.exceptions import ReadTimeout

from custom_components.spotcast.binary_sensor.abstract_binary_sensor import (
    SpotcastBinarySensor
)

LOGGER = getLogger(__name__)


class SpotifyProfileMalfunctionBinarySensor(SpotcastBinarySensor):
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

    GENERIC_NAME = "Spotify Profile Malfunction"
    ICON = "mdi:bug"
    ICON_OFF = "mdi:bug-check"
    INACTIVE_STATE = STATE_OK
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC

    async def async_update(self):

        try:
            profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout) as exc:
            LOGGER.error(exc)
            self._attr_state = STATE_PROBLEM
            return

        LOGGER.debug(
            "Getting Spotify Profile for account `%s`",
            self.account.name
        )

        LOGGER.debug(
            "Profile retrieve for account id `%s`", profile["id"],
        )

        self._attr_state = STATE_OK
