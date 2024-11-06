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


class DeviceNotFoundError(HomeAssistantError):
    """Raised when a device can't be found based on it's id"""


class AmbiguousDeviceId(HomeAssistantError):
    """Raised when the selection of an entity is ambiguous for a
    device"""


class UnmanagedSelectionError(HomeAssistantError):
    """Raised when a target selector provides a target selection
    that spotcast can't manage"""
