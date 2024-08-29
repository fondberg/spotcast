from test import hello_world
from logging import getLogger

DOMAIN = "spotcast"
LOGGER = getLogger(__name__)


def setup(hass, config) -> bool:
    """Initial setup of spotcast

    Returns:
        - bool: returns `True` if the integration setup was successfull
    """
    LOGGER.error(type(hass))
    LOGGER.error(type(config))
    LOGGER.error(hello_world())

    return True
