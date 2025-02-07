"""The IsDefaultBonarySensor object

Classes
    - IsDefaultBinarySensor
"""

from logging import getLogger

from homeassistant.components.binary_sensor import (
    EntityCategory
)
from homeassistant.const import STATE_OFF, STATE_ON

from custom_components.spotcast.binary_sensor.abstract_binary_sensor import (
    SpotcastBinarySensor
)

LOGGER = getLogger(__name__)


class IsDefaultBinarySensor(SpotcastBinarySensor):
    """Diagnostic binary sensor that confirms if the account is the
    default Spotcast account

    Methods:
        - async_update
    """

    GENERIC_NAME = "Default Account"
    GENERIC_ID = "is_default_account"
    ICON = "mdi:account-check"
    ICON_OFF = ICON
    ENTITY_CATEGORY = EntityCategory.DIAGNOSTIC

    async def _async_update_process(self):
        """Updates based on the is_default proerty of account
        asynchornously"""
        LOGGER.debug(
            "Updating default state sensor for `%s`",
            self.account.entry_id,
        )

        self._attr_state = STATE_ON if self.account.is_default else STATE_OFF
