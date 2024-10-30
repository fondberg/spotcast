"""Module for utility functions

Functions:
    - get_account_entry
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.services.exceptions import (
    AccountNotFoundError,
    NoDefaultAccountError,
)
from custom_components.spotcast import DOMAIN


def get_account_entry(
        hass: HomeAssistant,
        account_id: str = None
) -> ConfigEntry:
    """Returns the config entry of the account. Returns the
    default account if not specified

    Args:
        - hass(HomeAssistant): The Home Assistant Instance
        - account_id(str): The id of the spotify account to get
    """

    if account_id is not None:
        try:
            return hass.data[DOMAIN][account_id]
        except KeyError as exc:
            raise AccountNotFoundError(
                f"The account {account_id} could not be found. Known accounts "
                f"are {hass.data[DOMAIN]}."
            ) from exc

    for entry in hass.data[DOMAIN].values():

        entry: ConfigEntry
        if entry.data["is_default"]:
            return entry

    raise NoDefaultAccountError("No Default account could be found")
