"""Exceptions for the Spotify Module

Classes:
    - TokenError
    - ExpiredCookiesError
    - UnknownTokenError
    - InvalidCookiesError
    - NoAuthManagerError
    - ProfileNotLoadedError
"""

from homeassistant.exceptions import HomeAssistantError, ServiceValidationError


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


class PlaybackError(HomeAssistantError):
    """raised when playback failed due to an exception from Spotify"""


class ExpiredDatasetError(HomeAssistantError):
    """Raised when a dataset if retrived while expired"""


class SearchQueryError(ServiceValidationError):
    """Abstract exception for the Search Query Object"""


class InvalidFilterError(SearchQueryError):
    """Raised when a search query is built with invalid filters"""


class InvalidTagsError(SearchQueryError):
    """Raised when a search query is built with invalid filters"""


class InvalidItemTypeError(SearchQueryError):
    """Raised when a search query is built with an invalid item type
    """


class InvalidUriError(ServiceValidationError):
    """raised when an invalid uri is provided"""
