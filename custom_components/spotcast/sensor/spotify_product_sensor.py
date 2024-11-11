"""The SpotifyProductSensor object

Classes:
    - SpotifyProductSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor,
    EntityCategory,
)

LOGGER = getLogger(__name__)


class SpotifyProductSensor(SpotcastSensor):
    """A Home Assistant sensor reporting the subscription type for a
    Spotify Account

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

    GENERIC_NAME = "Spotify Product"
    ICON = "mdi:account-card"
    ICON_OFF = ICON
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC

    async def async_update(self):

        try:
            profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout):
            LOGGER.warn(
                "Failed to update Spotify Product sensor. Sensor know "
                "unavailable"
            )
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Getting Spotify Subscription Type `%s`",
            self.account.name
        )

        LOGGER.debug(
            "Account `%s` has the `%s` subscription",
            profile["id"],
            profile["product"],
        )

        self._attr_state = profile["product"]
