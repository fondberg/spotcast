from logging import getLogger
from time import sleep

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml.objects import NodeDictClass

from custom_components.spotcast.chromecast.device import ChromecastDevice

DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


def setup(hass: HomeAssistant, config: NodeDictClass) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """

    sleep(2)

    player = ChromecastDevice(hass, "media_player.atelier")

    return True
