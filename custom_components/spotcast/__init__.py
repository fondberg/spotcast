from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml.objects import NodeDictClass

from custom_components.spotcast.test import hello_world

DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


def setup(hass: HomeAssistant, config: NodeDictClass) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """
    LOGGER.error(hello_world())

    return True
