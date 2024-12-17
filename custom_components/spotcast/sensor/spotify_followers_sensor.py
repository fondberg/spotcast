"""The SpotifyFollowersSensor object

Classes:
    - SpotifyFollowersSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor
from custom_components.spotcast.sessions.exceptions import (
    UpstreamServerNotready
)

LOGGER = getLogger(__name__)


class SpotifyFollowersSensor(SpotcastSensor):
    """A Home Assistant sensor reporting the number of followers for
    an account

    properties:
        - state_class(str): the state class of the sensor

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Followers"
    ICON = "mdi:account-multiple"
    ICON_OFF = ICON
    UNITS_OF_MEASURE = "followers"

    async def async_update(self):
        """Updates the number of followers asynchornously"""
        try:
            self._profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout, UpstreamServerNotready):
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Getting Spotify followers for account `%s`",
            self.account.name
        )

        follower_count = self._profile["followers"]["total"]

        LOGGER.debug(
            "Found %d followers for spotify account `%s`",
            follower_count,
            self.account.name
        )

        self._attr_state = follower_count
