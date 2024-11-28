"""Module for the SpotifyAccount class"""

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from spotifyaio import SpotifyClient, Device


from custom_components.spotcast.spotify.spotify_data import SpotifyData
from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.utils import ensure_default_data
from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
    ConnectionSession,
    async_get_config_entry_implementation,
)

LOGGER = getLogger(__name__)


class SpotifyAccount:
    """The account of a Spotify user. Able to leverage both the
    public and private API

    Attributes:
        - entry_id(str): The id of the config entry linked to the
            account
        - is_default(bool): True if the account is current the default
            Spotcast Account

    Constants:
        - SCOPE(tuple[str]): the scope used for api calls
        - DJ_URI(str): The playlist uri for the DJ playlist

    Properties:
        - base_refresh_rate(int): The base refresh rate used by the
            account for dataset expiration
    """
    SCOPE = (
        "user-modify-playback-state",
        "user-read-playback-state",
        "user-read-private",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-read",
        "user-top-read",
        "user-read-playback-position",
        "user-read-recently-played",
        "user-follow-read",
    )

    DJ_URI = "spotify:playlist:37i9dQZF1EYkqdzj48dyYq"

    def __init__(
            self,
            entry_id: str,
            hass: HomeAssistant,
            public_session=OAuth2Session,
            private_session=InternalSession,
            is_default: bool = False,
            base_refresh_rate: int = 30,
    ):
        """The account of a Spotify user. Able to leverage both the
        public and private API

        Args:
            - entry_id(str): The id of the config entry in HomeAssistant
                for the account.
            - hass(HomeAssistant): The Home Assistant Instance
            - public_api(OAuth2Session): The public api session
                for the Spotify Account
            - private_api(InternalSession): The private api
                session for the Spotify Account
            - is_default(bool, optional): True if account is treated as
                default for service call. Defaults to False.
            - base_refresh_rate(int, optional): The base refresh rate
                used to update dateset
        """

        self.entry_id = entry_id
        self._hass = hass
        self.is_default = is_default
        self._base_refresh_rate = base_refresh_rate

        self._sessions: dict[str, ConnectionSession] = {
            "public": public_session,
            "private": private_session,
        }

        self.apis: dict[str, SpotifyClient] = {}

        for name, session in self._sessions.items():
            self.apis[name] = SpotifyClient(
                session,
                refresh_token_function=session.async_refresh_token
            )

        self._datasets = SpotifyData(self)

    @property
    def base_refresh_rate(self) -> int:
        """Returns the current base refresh rate """
        return self._base_refresh_rate

    @base_refresh_rate.setter
    def base_refresh_rate(self, value: int):
        """Sets the base refresh rate and updates the datasets
        accordingly"""
        self._base_refresh_rate = value
        self._datasets.update_refresh_rate()

    @property
    def health_status(self) -> dict[str, bool]:
        """Returns the health status of the underlying sessions"""
        health = {}

        for key, session in self._sessions.items():
            health[key] = session.is_healthy

        return health

    async def get_profile(self) -> dict:
        """Returns the active profile of the user"""
        dataset = self._datasets.get("profile")
        return await dataset.async_get()

    async def get_devices(self) -> list[Device]:
        """Returns the list of currently available devices"""
        dataset = self._datasets.get("devices")
        return await dataset.async_get()

    @staticmethod
    async def from_config_entry(
            hass: HomeAssistant,
            entry: ConfigEntry,
    ) -> "SpotifyAccount":
        """Builds a Spotify Account from a Home Assistant Config Entry

        Args:
            - hass(HomeAssistant): The Home Assistant instance
            - entry(ConfigEntry): the config entry for a spotify
                account

        Returns:
            - SpotifyAccount: A Spotify account with active tokens
                and sessions
        """

        hass = ensure_default_data(hass, entry.entry_id)
        data = hass.data[DOMAIN]

        account = data[entry.entry_id].get("account")

        if account is not None:
            LOGGER.debug(
                "Providing preexisting account from entry `%s`",
                entry.entry_id,
            )

        oauth_implementation = await async_get_config_entry_implementation(
            hass=hass,
            config_entry=entry,
        )

        # building sessions and ensure up to date tokens
        public_session = OAuth2Session(hass, entry, oauth_implementation)
        await public_session.async_ensure_token_valid()

        private_session = InternalSession(hass, entry)
        await private_session.async_ensure_token_valid()

        account = SpotifyAccount(
            entry_id=entry.entry_id,
            hass=hass,
            public_session=public_session,
            private_session=private_session,
            **entry.options
        )

        await account.get_profile()

        LOGGER.debug(
            "Adding entry `%s` to spotcast data entries",
            entry.entry_id
        )

        hass.data[DOMAIN][entry.entry_id]["account"] = account

        return account
