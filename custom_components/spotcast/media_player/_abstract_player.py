"""Abstract Media Player class for all iot media player type

Classes:
    - MediaPlayer
"""

from abc import ABC, abstractmethod
from logging import getLogger


LOGGER = getLogger(__name__)


class MediaPlayer(ABC):
    """Abstract Media Player class for all iot media player type

    Constants:
        - DOMAIN(str): the domain of device in HomeAssistant
        - PLATFORM(str): the name of the integration platform in
            HomeAssistant

    Functions:
        - from_hass
        - from_network
    """

    DOMAIN: str = "media_player"
    INTEGRATION: str = None

    @property
    @abstractmethod
    def id(self) -> str:
        """The spotify device id of the player"""
