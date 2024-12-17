"""The SpotifyProfileSensor object

Classes:
    - SpotifyProfileSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN, STATE_OK
from requests.exceptions import ReadTimeout

from custom_components.spotcast.utils import copy_to_dict
from custom_components.spotcast.sessions.exceptions import (
    UpstreamServerNotready
)

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor
)

LOGGER = getLogger(__name__)


class SpotifyProfileSensor(SpotcastSensor):
    """A Home Assistant sensor reporting information about the profile
    of a Spotify Account

    Properties:
        - entity_picture(str): the link to the entity picture for the
            sensor

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Profile"
    ICON = "mdi:account"
    DEFAULT_ATTRIBUTES = {}
    STATE_CLASS = None

    @property
    def entity_picture(self) -> str:
        """Link to the entity picture for the sensor"""
        if self.state == STATE_OK:
            return self.account.image_link

        return None

    async def async_update(self):
        """Updates the profile asynchornously"""
        try:
            profile = await self.account.async_profile()
        except (ReadTimeoutError, ReadTimeout, UpstreamServerNotready):
            self._attr_state = STATE_UNKNOWN
            self._attributes = {}
            return

        profile = copy_to_dict(profile)

        LOGGER.debug(
            "Getting Spotify Profile for account `%s`",
            self.account.name
        )

        LOGGER.debug(
            "Profile retrieve for account id `%s`", profile["id"],
        )

        self._attributes = self._clean_profile(profile)
        self._attributes["entry_id"] = self.account.entry_id
        self._attr_state = STATE_OK

    @staticmethod
    def _clean_profile(profile: dict) -> dict:
        """Cleans the profile for a better attributes result in Home
        Assistant

        Args:
            - profile(dict): the raw profile from Spotify API

        Returns:
            - dict: a clean profile for better
        """

        profile["filter_explicit_enabled"] = profile["explicit_content"][
            "filter_enabled"
        ]
        profile["filter_explicit_locked"] = profile["explicit_content"][
            "filter_locked"
        ]
        profile.pop("explicit_content")

        profile["followers_count"] = profile["followers"]["total"]
        profile.pop("followers")
        profile.pop("href")
        profile.pop("external_urls")
        profile.pop("images")

        return profile
