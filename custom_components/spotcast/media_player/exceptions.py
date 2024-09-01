"""Module for general media player exceptions"""

from homeassistant.exceptions import HomeAssistantError


class MediaPlayerError(HomeAssistantError):
    """Generic Exceptions for Media Player"""


class MediaPlayerNotFoundError(MediaPlayerError):
    """Error raised when the player could not be found"""


class InvalidPlatformError(MediaPlayerError):
    """Raised when the platform provided is invalid"""


class MissingDeviceTypeError(MediaPlayerError):
    """Raised when the device type os not set for the media player"""
