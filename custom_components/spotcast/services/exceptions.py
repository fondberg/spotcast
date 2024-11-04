"""Module with exceptions for servivce calls

Classes:
    - AccountNotFoundError
    - NoDefaultAccountError
    - UnknownServiceError
"""

from homeassistant.exceptions import HomeAssistantError


class AccountNotFoundError(HomeAssistantError):
    """Raised when the account id provided could not be found in
    currently set accounts"""


class NoDefaultAccountError(HomeAssistantError):
    """Raised if there are no default account to be found"""


class UnknownServiceError(HomeAssistantError):
    """Raised if the service name called is not known to spotcast"""


class TooManyMediaPlayersError(HomeAssistantError):
    """Raised when too many media players are in a service call"""
