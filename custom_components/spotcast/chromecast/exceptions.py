"""Module containing exceptions for the chromecast protocol

Classes:
    - AppLaunchError
    - UnknownMessageError
"""

from homeassistant.exceptions import HomeAssistantError


class AppLaunchError(HomeAssistantError):
    """Raised when a chromecast application can't launch"""


class UnknownMessageError(HomeAssistantError):
    """Raised when an unknown message is recieved for chromecast
    registration"""
