"""Module for a custom implementation of the Oauth2Session due to
spotcast custom config data format

Classes:
    - PublicSession

Functions:
    - async_get_config_entry_implementation
"""

from typing import cast
from aiohttp import ClientError, ClientOSError, ClientResponseError
from aiohttp.client_exceptions import ClientConnectorError
from asyncio import Lock
from logging import getLogger

from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    client,
    async_oauth2_request,
)
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.config_entry_oauth2_flow import (
    AbstractOAuth2Implementation,
    async_get_implementations
)

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
)
from custom_components.spotcast.sessions.exceptions import (
    TokenRefreshError,
    UpstreamServerNotready,
)

LOGGER = getLogger(__name__)


class PublicSession(ConnectionSession, OAuth2Session):
    """Custom implementation of the OAuth2Session for Spotcast

    Properties:
        - token(dict): The current token for the public spotify api

    Methods:
        - async_ensure_token_valid
        - async_request
    """

    API_ENDPOINT = "https://api.spotify.com"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        implementation: AbstractOAuth2Implementation,
    ) -> None:
        """Initialize an OAuth2 session."""
        self.implementation = implementation
        super().__init__(hass, entry)

    @property
    def token(self) -> dict:
        """Return the token"""
        return cast(dict, self.entry.data["external_api"]["token"])

    @property
    def clean_token(self) -> str:
        """Returns the token only"""
        return self.token.get(CONF_ACCESS_TOKEN)

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the current token is valid"""
        not_ready = False
        async with self._token_lock:

            if not self.supervisor.is_ready:
                not_ready = True

            if self.valid_token:
                return

            else:

                try:
                    new_token = await self.implementation.async_refresh_token(
                        self.token
                    )
                    new_data = self.entry.data
                    new_data["external_api"]["token"] = new_token
                    self.entry.data["external_api"]["token"] = new_token

                    self.hass.config_entries.async_update_entry(
                        self.entry,
                        data=new_data,
                    )
                    self._is_healthy = True

                except self.supervisor.SUPERVISED_EXCEPTIONS as exc:
                    self.supervisor._is_healthy = False
                    self.supervisor.log_message(exc)
                    not_ready = True
                except ClientResponseError as exc:
                    LOGGER.error("Unable to refresh Spotify Public API Token")
                    raise TokenRefreshError(exc)

        if not_ready:
            raise UpstreamServerNotready("Server not ready for refresh")

    async def async_request(
            self,
            method: str,
            url: str,
            **kwargs
    ) -> client.ClientResponse:
        """Make a request"""
        await self.async_ensure_token_valid()
        return await async_oauth2_request(
            self.hass,
            self.entry.data["external_api"]["token"],
            method,
            url,
            **kwargs,
        )


async def async_get_config_entry_implementation(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> AbstractOAuth2Implementation:
    """Return the implementation for this config entry."""
    implementations = await async_get_implementations(
        hass,
        config_entry.domain
    )

    implementation = implementations.get(
        config_entry.data["external_api"]["auth_implementation"]
    )

    if implementation is None:
        raise ValueError("Implementation not available")

    return implementation
