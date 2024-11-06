"""Module for exceptions related to api sessions

Classes:
    - TokenRefreshError
    - ExpiredSpotifyCookiesError
"""

from homeassistant.exceptions import HomeAssistantError


class TokenRefreshError(HomeAssistantError):
    """Raised when a token refresh fails"""


class ExpiredSpotifyCookiesError(HomeAssistantError):
    """Raised if the sp_dc and sp_key are expired"""
