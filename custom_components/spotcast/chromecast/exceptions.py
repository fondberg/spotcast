"""Module containing exceptions for the chromecast protocol"""

from homeassistant.exceptions import HomeAssistantError


class AppLaunchError(HomeAssistantError):
    """Raised when a chromecast application can't launch"""
