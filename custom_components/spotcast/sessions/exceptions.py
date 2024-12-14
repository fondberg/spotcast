"""Module for exceptions related to api sessions

Classes:
    - TokenRefreshError
    - ExpiredSpotifyCookiesError
"""

from custom_components.spotcast.spotify.exceptions import TokenError


class TokenRefreshError(TokenError):
    """Raised when a token refresh fails"""


class ExpiredSpotifyCookiesError(TokenRefreshError):
    """Raised if the sp_dc and sp_key are expired"""
