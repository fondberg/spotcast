"""Module to manage the configuration flow for the integration"""

from logging import getLogger

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL
from homeassistant.helpers.config_entry_oauth2_flow import (
    async_get_implementations,
    async_get_application_credentials,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.spotify.config_flow import SpotifyFlowHandler
from homeassistant.components import http
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.spotify import SpotifyAccount

LOGGER = getLogger(__name__)


class SpotcastFlowHandler(SpotifyFlowHandler, domain=DOMAIN):

    DOMAIN = DOMAIN
    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    INTERNAL_API_SCHEMA = vol.Schema({
        vol.Required("sp_dc", default=""): str,
        vol.Required("sp_key", default=""): str,
    })

    @property
    def extra_authorize_data(self) -> dict[str]:
        """Extra data to append to authorization url"""
        return {"scope": ",".join(SpotifyAccount.SCOPE)}

    async def async_step_user(
        self,
        user_input: dict[str] = None,
    ) -> FlowResult:
        """Handles flwo initiated by the user interface"""

        LOGGER.debug("Config flow for domain `%s` initiated", self.DOMAIN)
        LOGGER.debug("Requesting Spotify Internal API credentials")

        return self.async_show_form(
            step_id="internal_api",
            data_schema=self.INTERNAL_API_SCHEMA
        )

    async def async_step_internal_api(
        self,
        user_input: dict[str] = None
    ) -> FlowResult:
        LOGGER.debug("Requesting OAuth Implementation setup")
        return self.async_step_pick_implementation(user_input)

    async def async_step_pick_implementation(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle a flow start."""
        implementations = await async_get_implementations(
            self.hass,
            self.DOMAIN
        )

        if user_input is not None and "implementation" in user_input:
            self.flow_impl = implementations[user_input["implementation"]]
            return await self.async_step_auth()

        if not implementations:
            if self.DOMAIN in await async_get_application_credentials(self.hass):
                return self.async_abort(reason="missing_credentials")
            return self.async_abort(reason="missing_configuration")

        req = http.current_request.get()
        if len(implementations) == 1 and req is not None:
            # Pick first implementation if we have only one, but only
            # if this is triggered by a user interaction (request).
            self.flow_impl = list(implementations.values())[0]
            return await self.async_step_auth()

        return self.async_show_form(
            step_id="pick_implementation",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "implementation", default=list(implementations)[0]
                    ): vol.In({key: impl.name for key, impl in implementations.items()})
                }
            ),
        )

    def _show_form(
        self,
        errors: str = None,
        step: str = "internal_api",
        user_data: dict = None,
    ) -> FlowResult:

        if step == "internal_api":
            return self.async_show_form(
                step_id="internal_api",
                data_schema=self.INTERNAL_API_SCHEMA
            )

        if step == "external_api":
            return self.async_step_pick_implementation(user_data)

        raise InvalidConfigStepError(
            f"`{step}` is not a valid configuration step. Open an issue "
            "in github"
        )


class InvalidConfigStepError(HomeAssistantError):
    """raised if an invalid config step is provided."""
