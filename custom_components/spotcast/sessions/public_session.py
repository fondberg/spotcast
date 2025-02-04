"""Module for a custom implementation of the Oauth2Session due to
spotcast custom config data format

Classes:
    - PublicSession

Functions:
    - async_get_config_entry_implementation
"""

from typing import cast
from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectorError
from asyncio import Lock

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
    InternalServerError,
)


class PublicSession(OAuth2Session, ConnectionSession):
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
        config_entry: ConfigEntry,
        implementation: AbstractOAuth2Implementation,
    ) -> None:
        """Initialize an OAuth2 session."""
        self.hass = hass
        self.config_entry = config_entry
        self.implementation = implementation
        self._is_healthy = False
        self._token_lock = Lock()

    @property
    def token(self) -> dict:
        """Return the token"""
        return cast(dict, self.config_entry.data["external_api"]["token"])

    @property
    def clean_token(self) -> str:
        """Returns the token only"""
        return self.token.get(CONF_ACCESS_TOKEN)

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the current token is valid"""
        async with self._token_lock:
            if self.valid_token:
                return

            try:
                new_token = await self.implementation.async_refresh_token(
                    self.token
                )
            except ClientConnectorError:
                self._is_healthy = False
                raise InternalServerError(
                    "Unable to connect to Spotify Public API"
                )
            except ClientError as exc:
                self._is_healthy = False
                raise TokenRefreshError(
                    "Unable to refresh Spotify Public API Token"
                ) from exc

            new_data = self.config_entry.data
            new_data["external_api"]["token"] = new_token
            self.config_entry.data["external_api"]["token"] = new_token

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data=new_data,
            )
            self._is_healthy = True

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
            self.config_entry.data["external_api"]["token"],
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
