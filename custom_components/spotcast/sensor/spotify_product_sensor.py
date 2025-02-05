"""The SpotifyProductSensor object

Classes:
    - SpotifyProductSensor
"""

from logging import getLogger


from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor,
    EntityCategory,
)

LOGGER = getLogger(__name__)


class SpotifyProductSensor(SpotcastSensor):
    """A Home Assistant sensor reporting the subscription type for a
    Spotify Account

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Product"
    ICON = "mdi:account-card"
    ICON_OFF = ICON
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC
    STATE_CLASS = None

    async def _async_update_process(self):
        """Updates the substription product asynchornously"""

        profile = await self.account.async_profile()

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
