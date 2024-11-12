"""Module for utility functions

Functions:
    - get_account_entry
"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from Levenshtein import ratio

from custom_components.spotcast.services.exceptions import (
    AccountNotFoundError,
    NoDefaultAccountError,
)
from custom_components.spotcast import DOMAIN
from custom_components.spotcast.exceptions import LowRatioError

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


def fuzzy_match(
    items: list[dict[str]] | str,
    search: str,
    key: str = None,
    threshold: float = 0.5
) -> dict:
    """Finds the best matched string based on a search term

    Args:
        - items(list[dict]): a list of dictionaries to match to a
            search term
        - search(str): the search term used for matching
        - key(str): the key item in the dictionary used to compare
            with the search term)
        - value(str): the key item in the dictionary to used as a
            return value
        - threshhold(float, optional): the minimum ratio to return a
            value. Defaults to 0.5

    Returns:
        - dict: the best match result

    Raises:
        - LowRatioError: raised if the best ratio is lower then the
            treshhold
    """

    best_ratio = -1
    best_item = None
    best_compared = None

    for item in items:

        compared = item

        if key is not None:
            compared = compared[key]

        current_ratio = ratio(search, compared)

        if current_ratio > best_ratio:
            best_ratio = current_ratio
            best_item = item
            best_compared = compared

    if best_ratio < threshold:
        raise LowRatioError(
            f"Best match for search term `{search}` is `{best_compared}` with "
            f"a ratio of {best_ratio:.3f}"
        )

    return best_item
