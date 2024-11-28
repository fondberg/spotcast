"""Module for the SpotifyAccount class

Classes:
    - SpotifyAccount
    - SpotifyData
"""

from logging import getLogger
from types import MappingProxyType
from typing import Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from spotifyaio import SpotifyClient, Device

from custom_components.spotcast.spotify.dataset import Dataset
from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.utils import ensure_default_data
from custom_components.spotcast.sessions import (
    PublicSession,
    PrivateSession,
    ConnectionSession,
    async_get_config_entry_implementation,
)

LOGGER = getLogger(__name__)

DATASETS = MappingProxyType({
    "devices": {
        "refresh_factor": 1,
        "can_expire": False,
    },
    "liked_songs": {
        "refresh_factor": 4,
        "can_expire": False,
    },
    "playlists": {
        "refresh_factor": 2,
        "can_expire": False,
    },
    "profile": {
        "refresh_factor": 10,
        "can_expire": True,
    },
    "categories": {
        "refresh_factor": 10,
        "can_expire": False,
    },
    "playback_state": {
        "refresh_factor": 1/2,
        "can_expire": False,
    }
})


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
            public_session=PublicSession,
            private_session=PrivateSession,
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
    def id(self) -> str:
        return "foo"

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

    async def _pager(
            self,
            function: Callable,
            prepends: list = None,
            appends: list = None,
            limit: int = 50,
            sub_layer: str = None,
            max_items: int = None,
    ) -> list[dict]:
        """Retrieves data from an api endpoint using pagination

        Args:
            - function(callable): the function to call to retrieve
                content. Must be able to take a `limit` and `offset`
                arguments.
            - preppends: arguments to pass to the function on
                each call before the limit and offset
            - appends: arguments to pass to the function on
                each call after the limit and offset
            - limit(int, optional): the maximum number of items to
                retrieve in a single call, defaults to 50
            - sub_layer(str, optional): sub key in the response
                containing the pagination. Use the response as a
                pagination if None. Defaults to None.
            - max_items(int, optional): the maximum number of items to
                retrieve. Retrieve all items if None. Defaults to None.

        Returns:
            - list[dict]: the list of liked songs for an account
        """

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
        public_session = PublicSession(hass, entry, oauth_implementation)
        await public_session.async_ensure_token_valid()

        private_session = PrivateSession(hass, entry)
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


class SpotifyData:
    """A collection of dataset for a spotify account"""

    def __init__(self, account: SpotifyAccount):

        self._account = account
        self._datasets: dict[str, Dataset] = {}

        functions = {
            "devices": account.apis["public"].get_devices,
            "liked_songs": account.apis["private"].get_saved_tracks,
            "playlists": account.apis[
                "private"
            ].get_playlists_for_current_user,
            "profile": account.apis["private"].get_current_user,
            "categories": account.apis["private"].get_categories,
            "playback_state": account.apis["private"].get_playback,
        }

        for name, arguments in DATASETS.items():
            function = functions.get(name)
            refresh_rate = self._account.base_refresh_rate
            refresh_rate *= arguments["refresh_factor"]
            can_expire = arguments["can_expire"]
            self._datasets[name] = Dataset(
                name=name,
                refresh_function=function,
                refresh_rate=refresh_rate,
                can_expire=can_expire
            )

    def update_refresh_rate(self):
        """Updates all datasets refresh rate according to the current
        base refresh rate of the account"""

        base_rate = self._account.base_refresh_rate

        for name, dataset in self._datasets.items():
            new_rate = base_rate * DATASETS[name]
            dataset.refresh_rate = new_rate

    def get(self, name: str) -> Dataset:
        """Retrieves a dataset"""
        return self._datasets[name]
