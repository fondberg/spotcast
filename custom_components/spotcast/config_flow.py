"""Module to manage the configuration flow for the integration"""

from homeassistant.config_entries import CONN_CLASS_CLOUD_POLL
from homeassistant.components.spotify.config_flow import SpotifyFlowHandler

from custom_components.spotcast import DOMAIN
from custom_components.spotcast.spotify import SpotifyAccount


class SpotcastFlowHandler(SpotifyFlowHandler, domain=DOMAIN):

    DOMAIN = DOMAIN
    VERSION = 1
    MINOR_VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    @property
    def extra_authorize_data(self) -> dict[str]:
        """Extra data to append to authorization url"""
        return {"scope": ",".join(SpotifyAccount.SCOPE)}
