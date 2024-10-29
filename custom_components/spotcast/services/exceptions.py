"""Module with exceptions for servivce calls"""

from homeassistant.exceptions import HomeAssistantError


class AccountNotFoundError(HomeAssistantError):
    """Raised when the account id provided could not be found in
    currently set accounts"""


class UnknownServiceError(HomeAssistantError):
    """Raised if the service name called is not known to spotcast"""
