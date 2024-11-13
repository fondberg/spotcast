"""Module with the option flow handler for spotcast

Classes:
    - SpotcastOptionsFlowHandler
"""

from logging import getLogger

import voluptuous as vol
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
                vol.Required("set_default"): bool
            }
        )
    }

    async def async_step_init(
        self,
        user_input: dict[str] | None = None
    ) -> FlowResult:
        return self.async_show_form(
            step_id="apply_default",
            data_schema=self.SCHEMAS["init"],
            errors={},
            last_step=True,
        )

    async def async_step_apply_default(
        self,
        user_input: dict[str]
    ) -> FlowResult:

        if not user_input["set_default"]:
            LOGGER.debug(
                "Config entry `%s` not set to default, skipping",
                self.config_entry.title,
            )
            return self.async_create_entry(title="", data={})

        if self.config_entry.data["is_default"]:
            LOGGER.info(
                "Config Entry `%s` already set to default spotcast account",
                self.config_entry.title
            )
            return self.async_create_entry(title="", data={})

        entries = self.hass.config_entries.async_entries(DOMAIN)
        old_default = None

        for entry in entries:
            entry_data = dict(entry.data)
            if entry.entry_id == self.config_entry.entry_id:
                continue

            is_default = entry.data["is_default"]
            entry_data["is_default"] = False

            if is_default:
                old_default = entry.title
                self.hass.data[DOMAIN][entry.entry_id]["account"]\
                    .is_default = False

            self.hass.config_entries.async_update_entry(entry, entry_data)

        LOGGER.info(
            "Switched Spotcast default account from `%s` to `%s`",
            old_default,
            self.config_entry.title,
        )

        new_data = dict(self.config_entry.data)
        new_data["is_default"] = True
        self.hass.data[DOMAIN][self.config_entry.entry_id]["account"]\
            .is_default = True

        self.async_create_entry(title=self.config_entry.title, data=new_data)
