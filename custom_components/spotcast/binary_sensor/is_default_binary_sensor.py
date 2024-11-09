"""The IsDefaultBonarySensor object

Classes
    - IsDefaultBinarySensor
"""

from logging import getLogger

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    EntityCategory
)
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNKNOWN

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class IsDefaultBinarySensor(BinarySensorEntity):
    """Diagnostic binary sensor that confirms if the account is the
    default Spotcast account
    """

    CLASS_NAME = "Spotcast Default Account Binary Sensor"

    def __init__(self, account: SpotifyAccount):
        """Initialise the is default binary sensor

        Args:
            - account(SpotifyAccount): The spotify account linked to
                the sensor
        """
        self.account = account

        LOGGER.debug(
            "Loading Spotcast Default Account Binary Sensor for %s",
            self.account.name,
        )

        self._attr_device_info = self.account.device_info
        self._attr_state = STATE_UNKNOWN
        self.entity_id = (
            f"sensor.{self.account.id}_is_default_spotcast_account"
        )
        self.entity_description = BinarySensorEntityDescription(
            key=self.entity_id,
            name=self.name,
            entity_category=EntityCategory.DIAGNOSTIC,
            has_entity_name=True,
        )

    @property
    def available(self) -> bool:
        return self._attr_state != STATE_UNKNOWN

    @property
    def is_on(self) -> bool | None:
        if self._attr_state == STATE_UNKNOWN:
            return None

        return self._attr_state == STATE_ON

    @property
    def icon(self) -> str:
        return "mdi:account-check"

    @property
    def name(self) -> str:
        return f"{self.account.id} Spotcast Default"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_is_default_spotcast_account"

    async def async_update(self):
        LOGGER.debug(
            "Updating default state sensor for `%s`",
            self.account.name,
        )

        self._attr_state = STATE_ON if self.account.is_default else STATE_OFF
