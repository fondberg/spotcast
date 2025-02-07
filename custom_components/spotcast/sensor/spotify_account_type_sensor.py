"""The SpotifyAccountTypeSensor object

Classes:
    - SpotifyAccountTypeSensor
"""

from logging import getLogger

from homeassistant.components.sensor import EntityCategory

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor

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

    async def _async_update_process(self):
        """Updates the account type asynchronously"""

        profile = await self.account.async_profile()

        LOGGER.debug(
            "Type retrieve for account id `%s`", profile["id"],
        )

        self._attr_state = profile["type"]
