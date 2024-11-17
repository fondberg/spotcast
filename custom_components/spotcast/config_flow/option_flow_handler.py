"""Module with the option flow handler for spotcast

Classes:
    - SpotcastOptionsFlowHandler
"""

from logging import getLogger

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import (
    OptionsFlowWithConfigEntry,
    FlowResult
)

from custom_components.spotcast import DOMAIN

LOGGER = getLogger(__name__)


class SpotcastOptionsFlowHandler(OptionsFlowWithConfigEntry):
    """Handles option configuration via the Integration page"""

    SCHEMAS = {
        "init": vol.Schema(
            {
                vol.Required("set_default"): bool,
                vol.Required("base_refresh_rate"): cv.positive_int,
            }
        )
    }

    async def async_step_init(
        self,
        user_input: dict[str] | None = None
    ) -> FlowResult:
        return self.async_show_form(
            step_id="apply_options",
            data_schema=self.add_suggested_values_to_schema(
                self.SCHEMAS["init"],
                self.config_entry.options
            ),
            errors={},
            last_step=True,
        )

    def set_default_user(self) -> dict:
        """Set the current user as default for spotcast"""

        if self.config_entry.options["is_default"]:
            LOGGER.info(
                "Config Entry `%s` already set to default spotcast account",
                self.config_entry.title
            )
            return

        entries = self.hass.config_entries.async_entries(DOMAIN)
        old_default = None

        for entry in entries:
            current_options = dict(entry.options)
            if entry.entry_id == self.config_entry.entry_id:
                continue

            is_default = current_options["is_default"]
            current_options["is_default"] = False

            if is_default:
                old_default = entry.title
                self.hass.data[DOMAIN][entry.entry_id]["account"]\
                    .is_default = False

            self.hass.config_entries.async_update_entry(
                entry,
                options=current_options
            )

        LOGGER.info(
            "Switching Default Spotcast account from `%s` to `%s`",
            old_default,
            self.config_entry.title,
        )
        self.config_entry.options["is_default"] = True

    def set_base_refresh_rate(self, new_refresh_rate: int):
        """Sets the base refresh rate for the account

        Args:
            - new_refresh_rate(int): the new refresh rate to set for
                the account
        """
        entry_id = self.config_entry.entry_id
        self.hass.data[DOMAIN][entry_id]["account"]\
            .base_refresh_rate = new_refresh_rate

        self.config_entry.options["base_refresh_rate"] = new_refresh_rate

    async def async_step_apply_options(
        self,
        user_input: dict[str]
    ) -> FlowResult:

        if user_input["set_default"]:
            self.set_default_user()

        self.set_base_refresh_rate(user_input["base_refresh_rate"])

        self.async_create_entry(title="", data={})
