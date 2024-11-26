"""Module for utility functions

Functions:
    - get_account_entry
"""

from logging import getLogger
from types import MappingProxyType

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from rapidfuzz.fuzz import ratio

from custom_components.spotcast.services.exceptions import (
    AccountNotFoundError,
    NoDefaultAccountError,
)
from custom_components.spotcast.const import DOMAIN
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

    Raises:
        - AccountNotFoundError: raised if No account can be found for
            entry_id provided
        - NoDefaultAccountError: raised if no default account exists
            for Spotcast
    """

    if account_id is not None:

        LOGGER.debug("Getting config entry for id `%s`", account_id)

        entry = hass.config_entries.async_get_entry(account_id)

        if entry is None:
            raise AccountNotFoundError(
                f"No entry found for id `{account_id}`"
            )

        return entry

    LOGGER.debug("Searching for default spotcast account")

    entries = hass.config_entries.async_entries(DOMAIN)

    for entry in entries:

        if entry.options["is_default"]:
            return entry

    raise NoDefaultAccountError("No Default account could be found")


def search_account(hass: HomeAssistant, search_term: str) -> "SpotifyAccount":
    """Searches for an account based on entry_id, account_id or name.
    Search is made in that order.

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - search_term(str): the search_term used to find the account.
            Either an entry id, account id or account name.

    Returns:
        - SpotifyAccount: the spotify account linked to the search term
    """

    accounts = {x: y["account"] for x, y in hass.data[DOMAIN].items()}

    search_lists = [
        accounts,
        {x.id: x for x in accounts.values()},
        {x.name: x for x in accounts.values()},
    ]

    for search_list in search_lists:
        account = search_list.get(search_term)

        if account is not None:
            return account

    raise AccountNotFoundError(
        f"Could not find an account that fits `{search_term}`. Ensure you use "
        "a valid entry id, account id or account name"
    )


def copy_to_dict(items: dict) -> dict:
    """Makes a deep copy of a dictionary"""

    if isinstance(items, (dict, MappingProxyType)):

        new_dict = {}

        for key, value in items.items():
            new_dict[key] = copy_to_dict(value)

        return new_dict

    if isinstance(items, list):

        new_list = []

        for item in items:
            new_list.append(copy_to_dict(item))

        return new_list

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

        current_ratio = ratio(search, compared)/100

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


def ensure_default_data(hass: HomeAssistant, entry_id: str) -> HomeAssistant:
    """Ensure the default dictionary is setup for the entry_id

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - entry_id(str): the id -f the entry being setup
    """

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    domain_data = hass.data[DOMAIN]

    if entry_id not in domain_data:
        domain_data[entry_id] = {}

    for key in ("account", "device_listener"):
        if key not in domain_data[entry_id]:
            domain_data[entry_id][key] = None

    return hass
