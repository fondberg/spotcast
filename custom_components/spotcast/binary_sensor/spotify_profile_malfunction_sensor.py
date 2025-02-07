"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger

from homeassistant.components.binary_sensor import EntityCategory
from homeassistant.const import STATE_OK, STATE_PROBLEM

from custom_components.spotcast.binary_sensor.abstract_binary_sensor import (
    SpotcastBinarySensor
)
from custom_components.spotcast.sensor.abstract_entity import POTENTIAL_ERRORS

LOGGER = getLogger(__name__)


class SpotifyProfileMalfunctionBinarySensor(SpotcastBinarySensor):
    """A Home Assistant sensor reporting information about the profile
    of a Spotify Account

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Profile Malfunction"
    ICON = "mdi:bug"
    ICON_OFF = "mdi:bug-check"
    INACTIVE_STATE = STATE_OK
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC

    async def _async_update_process(self):
        """The update process"""
        raise NotImplementedError(
            "Not implemented, use the `async_update` method directly"
        )

    async def async_update(self):
        """Updates the profile and mark a problem if failing
        asynchornously"""

        try:
            profile = await self.account.async_profile()
        except POTENTIAL_ERRORS as exc:
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
