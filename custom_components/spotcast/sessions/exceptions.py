"""Module for exceptions related to api sessions

Classes:
    - TokenRefreshError
    - ExpiredSpotifyCookiesError
"""

from homeassistant.exceptions import HomeAssistantError

from custom_components.spotcast.spotify.exceptions import TokenError


class TokenRefreshError(TokenError):
    """Raised when a token refresh fails"""


class ExpiredSpotifyCookiesError(TokenRefreshError):
    """Raised if the sp_dc and sp_key are expired"""


class InternalServerError(HomeAssistantError):
    """Raised when Spotify Server respond with an internal server
    error (range 500)
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

        super().__init__(message)


class UpstreamServerNotready(HomeAssistantError):
    """Raised when the upstream server is not ready to receive
    communication again"""
