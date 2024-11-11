"""Module for utility functions

Functions:
    - get_account_entry
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.util.read_only_dict import ReadOnlyDict

from custom_components.spotcast.services.exceptions import (
    AccountNotFoundError,
    NoDefaultAccountError,
)
from custom_components.spotcast import DOMAIN

LOGGER = getLogger(__name__)


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

        LOGGER.debug("Getting config entry for id `%s`", account_id)

        entry = hass.config_entries.async_get_entry(account_id)

        if entry is None:
            raise AccountNotFoundError(
                "No entry foind for id `%s`", account_id
            )

        return entry

    LOGGER.debug("Searching for default spotcast account")

    entries = hass.config_entries.async_entries(DOMAIN)

    for entry in entries:

        if entry.data["is_default"]:
            return entry

    raise NoDefaultAccountError("No Default account could be found")


def copy_to_dict(items: dict) -> dict:
    """Makes a deep copy of a dictionary"""

    if isinstance(items, dict):

        new_dict = {}

        for key, value in items.items():
            new_dict[key] = copy_to_dict(value)

        return new_dict

    elif isinstance(items, list):

        new_list = []

        for item in items:
            new_list.append(copy_to_dict(item))

        return new_list

    else:
        return items
