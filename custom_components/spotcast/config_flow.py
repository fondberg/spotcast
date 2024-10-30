"""Module to manage the configuration flow for the integration

Classes:
    - SpotcastFlowHandler
"""

from logging import getLogger
from typing import Any

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL
from homeassistant.helpers import config_validation as cv
from homeassistant.components.spotify.config_flow import SpotifyFlowHandler
import voluptuous as vol
from homeassistant.config_entries import ConfigFlowResult
from spotipy import Spotify

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.spotify import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotcastFlowHandler(SpotifyFlowHandler, domain=DOMAIN):

    DOMAIN = DOMAIN
    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    INTERNAL_API_SCHEMA = vol.Schema({
        vol.Required("sp_dc", default=""): cv.string,
        vol.Required("sp_key", default=""): cv.string
    })

    def __init__(self):
        self.data: dict = {}
        super().__init__()

    @property
    def extra_authorize_data(self) -> dict[str]:
        """Extra data to append to authorization url"""
        return {"scope": ",".join(SpotifyAccount.SCOPE)}

    async def async_step_internal_api(
            self,
            user_input: dict[str]
    ) -> ConfigFlowResult:
        """Manages the data entry from the internal api step"""
        LOGGER.debug("Adding internal api to entry data")
        self.data["internal_api"] = user_input
        return await self.async_oauth_create_entry(self.data)

    async def async_oauth_create_entry(
            self,
            data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Create an entry for Spotify."""

        if "external_api" not in self.data:
            LOGGER.debug("Adding external api to entry data")
            self.data["external_api"] = data

        if "internal_api" not in self.data:
            return self.async_show_form(
                step_id="internal_api",
                data_schema=self.INTERNAL_API_SCHEMA,
                errors={},
            )

        external_api = self.data["external_api"]

        spotify = Spotify(auth=external_api["token"]["access_token"])

        try:
            current_user = await self.hass.async_add_executor_job(
                spotify.current_user
            )
        except Exception:  # noqa: BLE001
            return self.async_abort(reason="connection_error")

        name = external_api["id"] = current_user["id"]

        if (
            self.reauth_entry
            and self.reauth_entry.data["id"] != current_user["id"]
        ):
            return self.async_abort(reason="reauth_account_mismatch")

        if current_user.get("display_name"):
            name = current_user["display_name"]

        self.data["name"] = name

        current_entries = self.hass.config_entries.async_entries(DOMAIN)

        self.data["is_default"] = len(current_entries) == 0

        await self.async_set_unique_id(current_user["id"])

        return self.async_create_entry(title=name, data=self.data)
