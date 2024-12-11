"""Module for websoket API utility functions"""

from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection
from homeassistant.exceptions import ServiceValidationError, HomeAssistantError

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.utils import get_account_entry, search_account

HANDLED_EXCEPTIONS = (ServiceValidationError, HomeAssistantError)


def websocket_wrapper(func: callable):

    async def wrapper(
        hass: HomeAssistant,
        connection: ActiveConnection,
        msg: dict
    ):
        try:
            return await func(hass, connection, msg)
        except HANDLED_EXCEPTIONS as exc:
            connection.send_error(msg["id"], type(exc).__name__, str(exc))

    return wrapper


async def async_get_account(hass: HomeAssistant, account: str = None) -> SpotifyAccount:
    """Retrieves a spotify account for a websocket query

    Args:
        - hass(HomeAssistant): the Home Assistant Instance
        - account_id(str, optional): the account to retrieve. Either
            an entry ud or an account id or name. If None, retrives the
            default account. Defaults to None.

    Return:
        - SpotifyAccount: A spotify account
    """

    if account is not None:
        return search_account(hass, account)

    entry = get_account_entry(hass)
    return await SpotifyAccount.async_from_config_entry(hass, entry)
