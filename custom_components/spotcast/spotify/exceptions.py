"""Exceptions for the Spotify Module"""

from homeassistant.exceptions import HomeAssistantError


class ExpiredCookiesError(HomeAssistantError):
    """Raised when valid cookies are expired"""


class UnknownTokenError(HomeAssistantError):
    """Raised when an error occurs while getting a spotify Token"""


class InvalidCookiesError(HomeAssistantError):
    """Raised in the case of invalid cookies provided"""
