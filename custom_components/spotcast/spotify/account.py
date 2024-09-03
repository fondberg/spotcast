"""Module for the spotify accout class"""

from logging import getLogger
from asyncio import get_running_loop, new_event_loop, set_event_loop

from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from spotipy import Spotify

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
        self.session: OAuth2Session = None

    async def async_connect(self) -> dict:
        """Tests the connection and returns the current user profile"""
        loop = get_running_loop()
        LOGGER.debug("Getting Profile from Spotify")
        profile = await loop.run_in_executor(None, self._spotify.me)
        self.name = profile["display_name"]
        return profile

    async def async_devices(self):
        loop = get_running_loop()
        devices = await loop.run_in_executor(None, self._spotify.devices)
        return devices

    def get_token(self) -> str:
        """Returns a valid token according to the auth system in place
        """
        if self.session is not None:
            LOGGER.debug("getting token from %s", self.session)
            return self.session.token["access_token"]

        raise NoAuthManagerError(
            "No Valid Authentication Manager could be found"
        )

    @staticmethod
    def from_oauth_session(
        session: OAuth2Session,
        country: str = None,
    ) -> "SpotifyAccount":
        """Builds a SpotifyAccount from a Home Assistant OAuth Session"""

        spotify = Spotify(auth=session.token["access_token"])

        account = SpotifyAccount(spotify, country=country)
        account.session = session

        return account
