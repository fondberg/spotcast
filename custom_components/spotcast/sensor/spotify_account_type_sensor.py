"""The SpotifyAccountTypeSensor object

Classes:
    - SpotifyAccountTypeSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    EntityCategory,
)
from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotifyAccountTypeSensor(SensorEntity):
    """A Home Assistant sensor reporting information about the type
    of Spotify Account

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

    CLASS_NAME = "Spotify Account Type Sensor"

    def __init__(self, account: SpotifyAccount):
        """A Home Assistant sensor reporting the type of Spotify
        Account

        Args:
            - account(SpotifyAccount): The spotify account probed by
                the sensor
        """
        self.account = account

        LOGGER.debug(
            "Loading Spotify Account Type sensor for %s",
            self.account.name
        )

        self._attr_device_info = self.account.device_info

        self._playlists = []
        self._attr_state = STATE_UNKNOWN
        self.entity_id = f"sensor.{self.account.id}_spotify_account_type"
        self._profile = {}
        self.entity_description = SensorEntityDescription(
            key=self.entity_id,
            name=self.name,
            entity_category=EntityCategory.DIAGNOSTIC,
            has_entity_name=True,
        )

    @property
    def icon(self) -> str:
        return "mdi:account"

    @property
    def name(self) -> str:
        return f"{self.account.name} Spotify Account Type"

    @property
    def unique_id(self) -> str:
        return f"{self.account.id}_spotify_account_type"

    @property
    def state(self) -> str:
        return self._attr_state

    async def async_update(self):
        LOGGER.debug(
            "Getting Spotify account type for `%s`",
            self.account.name
        )

        try:
            self._profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            return

        LOGGER.debug(
            "Type retrieve for account id `%s`", self._profile["id"],
        )

        self._attr_state = self._profile["type"]
