"""The SpotifyFollowersSensor object

Classes:
    - SpotifyFollowersSensor
"""

from logging import getLogger

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor

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

    async def _async_update_process(self):
        """Updates the number of followers asynchornously"""
        self._profile = await self.account.async_profile()

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
