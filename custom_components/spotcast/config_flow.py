"""Module to manage the configuration flow for the integration

Classes:
    - SpotcastFlowHandler
"""

from logging import getLogger
from typing import Any
from unittest.mock import MagicMock
from types import MappingProxyType

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL
from homeassistant.helpers import config_validation as cv
from homeassistant.components.spotify.config_flow import SpotifyFlowHandler
from homeassistant.config_entries import (
    ConfigFlowResult,
    OptionsFlow,
    ConfigEntry,
    FlowResult,
    SOURCE_REAUTH,
)
import voluptuous as vol
from spotipy import Spotify

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.utils import copy_to_dict
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.sessions import PrivateSession

LOGGER = getLogger(__name__)

DEFAULT_OPTIONS = MappingProxyType({
    "is_default": False,
    "base_refresh_rate": 30,
})


class SpotcastOptionsFlowHandler(OptionsFlow):
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
        user_input: dict[str] | None = None,
    ) -> FlowResult:
        """Initial Step for the Option Configuration Flow"""

        options = copy_to_dict(self.config_entry.options)

        LOGGER.debug("Opening Config menu for `%s`", self.config_entry.title)

        self._options = DEFAULT_OPTIONS | options

        LOGGER.debug("Options set to `%s`", self._options)

        return self.async_show_form(
            step_id="apply_options",
            data_schema=self.add_suggested_values_to_schema(
                self.SCHEMAS["init"],
                self._options,
            ),
            errors={},
        )

    def set_default_user(self) -> dict:
        """Set the current user as default for spotcast"""

        entries = self.hass.config_entries.async_entries(DOMAIN)
        old_default = None

        for entry in entries:

            is_default = entry.options["is_default"]
            options = copy_to_dict(entry.options)
            options["is_default"] = False

            if is_default:
                old_default = entry.title
                self.hass.data[DOMAIN][entry.entry_id]["account"]\
                    .is_default = False

            self.hass.config_entries.async_update_entry(
                entry,
                options=options,
            )

        LOGGER.info(
            "Switching Default Spotcast account from `%s` to `%s`",
            old_default,
            self.config_entry.title,
        )

        self._options["is_default"] = True
        self.hass.data[DOMAIN][self.config_entry.entry_id]["account"]\
            .is_default = True

    def set_base_refresh_rate(self, new_refresh_rate: int):
        """Sets the base refresh rate for the account

        Args:
            - new_refresh_rate(int): the new refresh rate to set for
                the account
        """

        if new_refresh_rate == self._options["base_refresh_rate"]:
            LOGGER.debug("Same refresh rate. Skipping")
            return

        LOGGER.info(
            "Setting spotcast entry `%s` to a base refresh rate of %d",
            self.config_entry.title,
            new_refresh_rate,
        )
        entry_id = self.config_entry.entry_id
        self.hass.data[DOMAIN][entry_id]["account"]\
            .base_refresh_rate = new_refresh_rate

        self._options["base_refresh_rate"] = new_refresh_rate

    async def async_step_apply_options(
        self,
        user_input: dict[str]
    ) -> FlowResult:
        """Step to apply the options configured"""

        if user_input["set_default"]:
            self.set_default_user()

        self.set_base_refresh_rate(user_input["base_refresh_rate"])

        self.hass.config_entries.async_update_entry(
            self.config_entry,
            options=self._options,
        )

        return self.async_abort(reason="Successfull")


class SpotcastFlowHandler(SpotifyFlowHandler, domain=DOMAIN):
    """Hnadler of the Config Flow for Spotcast

    Attributes:
        - data(dict): The set of information currently collected for
            the entry

    Constants:
        - DOMAIN(str): The domain of flow is linked to
        - VERSION(int): The major version of the config
        - MINOR_VERSION(int): the minor version of the config
        - CONNECTION_CLASS(str): The type of integration being setup
        - INTERNAL_API_SCEHMA(vol.Schema): the schema for the
            internal api setup

    Properties:
        - extra_authorize_data(dict[str]): Provides additional
            information required for the OAuth authorisation

    Methods:
        - async_step_internal_api
        - async_oauth_create_entry
        - async_step_reauth_confirm

    Functions:
        - async_get_options_flow
    """

    DOMAIN = DOMAIN
    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    INTERNAL_API_SCHEMA = vol.Schema({
        vol.Required("sp_dc", default=""): cv.string,
        vol.Required("sp_key", default=""): cv.string
    })

    def __init__(self):
        """Constructor of the Spotcast Config Flow"""
        self.data: dict = {}
        self._import_data = None
        super().__init__()

    @property
    def extra_authorize_data(self) -> dict[str]:
        """Extra data to append to authorization url"""
        return {"scope": ",".join(SpotifyAccount.SCOPE)}

    async def async_step_import(
        self,
        import_config: dict
    ) -> ConfigFlowResult:
        """Step for importing a config entry from yaml to ui"""
        LOGGER.info("Importing YAML configuration for Spotcast")
        LOGGER.warn("In import step")

        self.context["import_data"] = {
            "sp_dc": import_config.get("sp_dc"),
            "sp_key": import_config.get("sp_key"),
        }
        return self.async_show_form(
            step_id="pick_implementation",
            data_schema=vol.Schema({}),
        )

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

        LOGGER.warn(self.context)

        if "external_api" not in self.data:
            LOGGER.debug("Adding external api to entry data")
            self.data["external_api"] = data

        if "import_data" in self.context:
            self.data["internal_api"] = self.context["import_data"].copy()
            LOGGER.debug("Adding internal API details from YAML import")

        if "internal_api" not in self.data:
            return self.async_show_form(
                step_id="internal_api",
                data_schema=self.INTERNAL_API_SCHEMA,
                errors={},
            )

        external_api = self.data["external_api"]

        # create a mock config able to mimmick a config entry for the
        # purpose of InternalSession
        entry = MagicMock(spec=ConfigEntry)
        entry.data = self.data
        private_session = PrivateSession(self.hass, entry)

        try:
            LOGGER.debug("loading curent user data")
            await private_session.async_ensure_token_valid()
            accounts: dict[str, Spotify] = {
                "public": Spotify(auth=external_api["token"]["access_token"]),
                "private": Spotify(auth=private_session.clean_token)
            }

            profiles = {}

            for key, account in accounts.items():
                profiles[key] = await self.hass.async_add_executor_job(
                    account.current_user
                )

        except Exception:  # pylint: disable=W0718
            return self.async_abort(reason="connection_error")

        ids = [x["id"] for x in profiles.values()]

        if ids[0] != ids[1]:
            return self.async_abort(reason="public_private_accounts_mismatch")

        current_user = profiles["public"]

        name = external_api["id"] = current_user["id"]
        display_name = current_user.get("display_name")

        if display_name is not None:
            name = current_user["display_name"]

        self.data["name"] = name

        await self.async_set_unique_id(current_user["id"])

        if self.source == SOURCE_REAUTH:
            self._abort_if_unique_id_mismatch(reason="reauth_account_mismatch")
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(), title=name, data=self.data
            )

        self._abort_if_unique_id_configured()
        current_entries = self.hass.config_entries.async_entries(DOMAIN)

        options = {
            "is_default": len(current_entries) == 0,
            "base_refresh_rate": 30,
        }

        return self.async_create_entry(
            title=name,
            data=self.data,
            options=options,
        )

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth dialog."""
        reauth_entry = self._get_reauth_entry()

        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                description_placeholders={
                    "account": reauth_entry.data["external_api"]["id"]
                },
                errors={},
            )

        return await self.async_step_pick_implementation(
            user_input={
                "implementation": reauth_entry.data[
                    "external_api"
                ]["auth_implementation"]}
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: ConfigEntry
    ) -> SpotcastOptionsFlowHandler:
        """Tells Home Assistant this integration supports configuration
        options"""
        return SpotcastOptionsFlowHandler()
