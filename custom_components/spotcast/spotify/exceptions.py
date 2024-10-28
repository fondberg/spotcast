"""Exceptions for the Spotify Module"""

from homeassistant.exceptions import HomeAssistantError


class TokenError(HomeAssistantError):
    """Generic Error with the Spotify Token"""


class ExpiredCookiesError(TokenError):
    """Raised when valid cookies are expired"""


class UnknownTokenError(TokenError):
    """Raised when an error occurs while getting a spotify Token"""


class InvalidCookiesError(TokenError):
    """Raised in the case of invalid cookies provided"""


class NoAuthManagerError(TokenError):
    """The Spotify Account has no Authentication manager in place"""


class ProfileNotLoadedError(HomeAssistantError):
    """Raised when the profile is not yet loaded"""
