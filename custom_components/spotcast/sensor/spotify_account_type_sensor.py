"""The SpotifyAccountTypeSensor object

Classes:
    - SpotifyAccountTypeSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import (
    EntityCategory,
)
from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor
)

LOGGER = getLogger(__name__)


class SpotifyAccountTypeSensor(SpotcastSensor):
    """A Home Assistant sensor reporting information about the type
    of Spotify Account

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Account Type"
    ICON = "mdi:account"
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC
    STATE_CLASS = None

    async def async_update(self):
        """Updates the account type asynchronously"""

        try:
            profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Getting Spotify account type for `%s`",
            self.account.name
        )

        LOGGER.debug(
            "Type retrieve for account id `%s`", profile["id"],
        )

        self._attr_state = profile["type"]
