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

from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer
)

from custom_components.spotcast.media_player.exceptions import (
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

    INTEGRATION = "cast"

    @property
    def id(self) -> str:
        """Returns the spotify id of the player"""
        return md5(self.name.encode()).hexdigest()
