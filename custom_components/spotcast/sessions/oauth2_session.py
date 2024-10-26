"""Module for a custom implementation of the Oauth2Session due to
spotcast custom config data format"""

from typing import cast

from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session as ParentOAuth2Session,
    client,
    async_oauth2_request,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.config_entry_oauth2_flow import (
    AbstractOAuth2Implementation,
    async_get_implementations
)

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
)


class OAuth2Session(ParentOAuth2Session, ConnectionSession):

    @property
    def token(self) -> dict:
        """Return the token"""
        return cast(dict, self.config_entry.data["external_api"]["token"])

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the current token is valid"""
        async with self._token_lock:
            if self.valid_token:
                return

            new_token = await self.implementation.async_refresh_token(
                self.token
            )

            new_data = self.config_entry.data
            new_data["external_api"]["token"] = new_token

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data=new_data,
            )

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
