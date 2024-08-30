"""Module containing exceptions specific to the chromecast module"""

from homeassistant.exceptions import HomeAssistantError


class EntityNotFoundError(HomeAssistantError):
    """Raised when an entity id can't be found"""


class NotCastCapableError(HomeAssistantError):
    """Raised when a device is not capable of chromecast protocal"""
