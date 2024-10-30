"""Module containing the chromecast media player implementation"""

from logging import getLogger
from uuid import UUID
from hashlib import md5

from pychromecast import (
    Chromecast as ParentChromecast,
    HostServiceInfo,
    CastInfo,
)

import pychromecast  # pylint: disable=unused-import

from homeassistant.core import HomeAssistant
from homeassistant.components.cast.media_player import CastDevice
from homeassistant.components.cast.helpers import ChromeCastZeroconf

from custom_components.spotcast.media_players._abstract_player import (
    MediaPlayer
)

from custom_components.spotcast.media_players.exceptions import (
    MediaPlayerNotFoundError
)

LOGGER = getLogger(__name__)


class Chromecast(ParentChromecast, MediaPlayer):
    """A chromecast media player

    Constants:
        - PLATFORM(str): the Home Assistant platform hosting the
            devices
        - DEVICE_TYPE(type): the type of device searched for

    Properties:
        - id: the spotify device if for the player

    functions:
        - from_hass
        - from_network
    """

    PLATFORM = "cast"
    DEVICE_TYPE = CastDevice

    @classmethod
    def from_hass(
            cls,
            hass: HomeAssistant,
            device_id: str,
            is_device_name: bool = False,
    ) -> "Chromecast":
        """Imports a Chromecast Player instance from Home Assistant

        Args:
            - hass(HomeAssistant): the home assistant server
            - device_id(str): the identifier of the device. Can be an
                entity id or a device name. See is_device_name
                arguments for more details.
            - is_device_name(bool, optional): If True, treats the
                device_id as the device name. Otherwise treats it as
                an entity_id. Defaults to False.

        Raises:
            - MediaPlayerNotFoundError: Raised if the player could not
                be found
        """
        devices: dict[str, CastDevice] = Chromecast\
            ._get_entities_from_platforms(hass, is_device_name)

        try:
            device = devices[device_id]
        except KeyError as exc:
            raise MediaPlayerNotFoundError(
                f"{device_id} could not be found inside integration "
                f"{cls.PLATFORM}"
            ) from exc

        LOGGER.debug("Found matching entity %s", device)
        LOGGER.debug("Casting info %s", device._cast_info.cast_info)

        cast_device = Chromecast(
            device._cast_info.cast_info,
            zconf=ChromeCastZeroconf.get_zeroconf(),
        )

        return cast_device

    @property
    def id(self) -> str:
        """Returns the spotify id of the player"""
        return md5(self.name.encode()).hexdigest()

    @staticmethod
    def from_network(
            host: str,
            port: int = 8009,
            uuid: UUID = None,
            model_name: str = None,
            friendly_name: str = None,
            manufacturer: str = None,
    ):

        services = {HostServiceInfo(host, port)}

        cast_info = CastInfo(
            services=services,
            uuid=uuid,
            model_name=model_name,
            friendly_name=friendly_name,
            host=host,
            port=port,
            cast_type=None,
            manufacturer=manufacturer,
        )

        device = Chromecast(cast_info)

        return device
