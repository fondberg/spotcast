"""Module containing the chromecast device class

Classes:
    - ChromecastDevice
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.components.cast.media_player import CastDevice
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.cast.helpers import ChromeCastZeroconf
from pychromecast import get_chromecast_from_cast_info

from custom_components.spotcast.chromecast.utils import extract_media_players
from custom_components.spotcast.chromecast.exceptions import (
    EntityNotFoundError,
    NotCastCapableError,
)


LOGGER = getLogger(__name__)


class ChromecastDevice:
    """A chromecast device

    Attributes:
        - entity_id(str): the unique entity id of the device
        - name(str): the friendly name of the device
        - cast_device(CastDevice): the pychromecast cast device

    Constants:
        - CAST_INTEGRATION(str): the name for the chromecast
            integration in HomeAssistant

    methods:
        - ...

    functions:
        - get_hass_devices
    """

    CAST_INTEGRATION = "cast"

    def __init__(self, hass: HomeAssistant, entity_id: str):
        """Constructor of the ChromecastDevice

        Args:
            - hass(HomeAssistant): the home assistant server
            - entity_id(str): the entity_id of the device to create

        Raises:
            - 
        """

        # check for existence of entity_id
        entity_state = hass.states.get(entity_id)

        if entity_state is None:
            raise EntityNotFoundError(f"Could not find entity `{entity_id}`")

        self.entity_id = entity_id
        self.name = entity_state.attributes.get("friendly_name")

        try:
            cast_device = ChromecastDevice.get_hass_devices(hass)[entity_id]
        except KeyError as exc:
            raise NotCastCapableError(
                f"Could not find `{entity_id}` as a registered cast media "
                "player"
            ) from exc

        LOGGER.debug(
            "Found `%s` with cast_info `%s`",
            entity_id,
            cast_device._cast_info
        )

        self.cast_device = get_chromecast_from_cast_info(
            cast_device._cast_info.cast_info,
            ChromeCastZeroconf.get_zeroconf(),
        )

        LOGGER.info("Waiting for `%s` to be ready", self.entity_id)
        self.cast_device.wait()
        LOGGER.info("Device `%s` is ready", self.entity_id)

    @staticmethod
    def get_hass_devices(
        hass: HomeAssistant,
        by_device_name: bool = False,
    ) -> dict[str, CastDevice]:
        """retrives a dictionary of media player integrated into home
        assistant

        Args:
            - hass(HomeAssistant): the Home Assistant server
            - by_device_name(bool, optional): Sets the dictionary key
                to the device name instead of the entity id. Defaults
                to False

        Returns:
            - dict[str, CastDevice]: a dictionary of CastDevice using
                the entity_id as the key, or device_name if
                `by_device_name` is set to True.
        """

        platforms = entity_platform.async_get_platforms(
            hass,
            ChromecastDevice.CAST_INTEGRATION
        )

        LOGGER.debug("platform retrieved: %s", platforms)

        devices = {}

        for platform in platforms:

            if platform.domain != "media_player":
                continue

            LOGGER.debug(
                "Found platform `%s` with domain `media_player`",
                platform
            )

            current_devices = extract_media_players(platform)

            if by_device_name:
                current_devices = {
                    x._name: x
                    for x in current_devices.values()
                }

            devices = devices | current_devices

        return devices
