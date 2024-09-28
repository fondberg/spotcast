"""Module for the spotify accout class"""

from logging import getLogger
from typing import Any, Callable
from asyncio import get_running_loop

from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from spotipy import Spotify, SpotifyOAuth

from custom_components.spotcast.spotify.exceptions import NoAuthManagerError


LOGGER = getLogger(__name__)


class SpotifyAccount:
    """A Spotify Account with the cookies information

    Attributes:
        - country(str): The ISO3166-2 country code for the account
        - name(str): Name of the account. Used for distinguishing
            between accounts when calling services
    """

    SCOPE = [
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
    ]

    def __init__(
            self,
            spotify: Spotify,
            country: str = None,
    ):
        self.name = None
        self.country = country
        self._spotify = spotify
        self.auth_manager: OAuth2Session | SpotifyOAuth = None

    def connect(self) -> dict:
        """Tests the connection and returns the current user profile"""
        LOGGER.debug("Getting Profile from Spotify")
        profile = self._spotify.me()
        LOGGER.debug("Profile retrived for user %s", profile["display_name"])
        self.name = profile["display_name"]
        return profile

    def devices(self):
        """Returns the list of devices"""
        LOGGER.debug("Getting Devices for account `%s`", self.name)
        devices = self._spotify.devices()["devices"]

        # Log all the devices found
        for device in devices:
            LOGGER.debug("Found Device [%s](%s)", device["name"], device["id"])

        return devices

    @staticmethod
    async def _async_wrapper(func: Callable, *args) -> Any:
        """Wrapper to execute a function inside an executor

        Args:
            - func(Callable): the function to run
            - *args: arguments to send to the function

        Return:
            - Any: the result of the function
        """
        loop = get_running_loop()
        return await loop.run_in_executor(None, func, *args)

    async def async_connect(self) -> dict:
        """Tests the connection and returns the current user profile"""
        return await self._async_wrapper(self.connect)

    async def async_devices(self):
        """Returns the list of devices"""
        return await self._async_wrapper(self.devices)

    def get_token(self) -> str:
        """Returns a valid token according to the auth system in place
        """
        if isinstance(self.auth_manager, (OAuth2Session, SpotifyOAuth)):
            LOGGER.debug("getting token from Hass %s", type(self.auth_manager))
            return self.auth_manager.token["access_token"]

        raise NoAuthManagerError(
            "No Valid Authentication Manager could be found"
        )

    @staticmethod
    def from_hass_oauth(
        session: OAuth2Session,
        country: str = None,
    ) -> "SpotifyAccount":
        """Builds a SpotifyAccount from a Home Assistant OAuth Session"""

        spotify = Spotify(auth=session.token["access_token"])

        account = SpotifyAccount(spotify, country=country)
        account.auth_manager = session

        return account

    @staticmethod
    def from_spotipy_oauth(
            spotipy_oauth: SpotifyOAuth,
            country: str = None,
    ) -> "SpotifyAccount":
        """Builds a SpotifyAccount from a Spotipy Local OAuth Session"""

        spotify = Spotify(auth_manager=spotipy_oauth)

        account = SpotifyAccount(spotify, country)
        account.auth_manager = spotipy_oauth

        return account
