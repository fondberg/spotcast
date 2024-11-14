"""Module with exceptions for servivce calls

Classes:
    - AccountNotFoundError
    - NoDefaultAccountError
    - UnknownServiceError
"""

from homeassistant.exceptions import HomeAssistantError, ServiceValidationError


class AccountNotFoundError(ServiceValidationError):
    """Raised when the account id provided could not be found in
    currently set accounts"""


class NoActivePlaybackError(ServiceValidationError):
    """Raised when there is no active playback for an account, while
    trying to call a service that requires active playback"""


class NoDefaultAccountError(HomeAssistantError):
    """Raised if there are no default account to be found"""


class UnknownServiceError(ServiceValidationError):
    """Raised if the service name called is not known to spotcast"""


class TooManyMediaPlayersError(ServiceValidationError):
    """Raised when too many media players are in a service call"""


class DeviceNotFoundError(ServiceValidationError):
    """Raised when a device can't be found based on it's id"""


class AmbiguousDeviceIdError(ServiceValidationError):
    """Raised when the selection of an entity is ambiguous for a
    device"""


class UnmanagedSelectionError(ServiceValidationError):
    """Raised when a target selector provides a target selection
    that spotcast can't manage"""


class InvalidCategoryError(ServiceValidationError):
    """Raised when an invalid category id is provided"""
