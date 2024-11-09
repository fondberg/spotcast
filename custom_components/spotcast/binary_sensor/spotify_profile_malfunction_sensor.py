"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    EntityCategory,
    BinarySensorDeviceClass,
)
from homeassistant.const import STATE_UNKNOWN, STATE_OK, STATE_PROBLEM
from requests.exceptions import ReadTimeout

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotifyProfileMalfunctionBinarySensor(BinarySensorEntity):
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

    CLASS_NAME = "Spotify Profile Malfunction Binary Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting the profile for a
        Spotify Account

        Args:
            - account(SpotifyAccount): The spotify account probed by
                the sensor
        """
        self.account = account

        LOGGER.debug(
            "Loading Spotify Playlists sensor for %s",
            self.account.name
        )

        self._attr_device_info = self.account.device_info

        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"binary_sensor.{self.account.id}_spotify_profile"
        self.entity_description = BinarySensorEntityDescription(
            key=self.entity_id,
            name=self.name,
            entity_category=EntityCategory.DIAGNOSTIC,
            device_class=BinarySensorDeviceClass.PROBLEM,
            has_entity_name=True,
        )

    @property
    def icon(self) -> str:
        if self._attr_state == STATE_OK:
            return "mdi:bug-check"

        return "mdi:bug"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Profile Malfunction"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_profile_malfunction"

    @property
    def available(self) -> bool:
        return self._attr_state != STATE_UNKNOWN

    @property
    def is_on(self) -> bool | None:
        if self._attr_state == STATE_UNKNOWN:
            return None

        return self._attr_state == STATE_PROBLEM

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify Profile for account `%s`",
            self.account.name
        )

        try:
            self._profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout) as exc:
            LOGGER.error(exc)
            self._attr_state = STATE_PROBLEM
            return

        LOGGER.debug(
            "Profile retrieve for account id `%s`", self._profile["id"],
        )

        self._attr_state = STATE_OK
