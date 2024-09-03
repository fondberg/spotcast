"""Module for the spotify accout class"""

from logging import getLogger
from asyncio import get_running_loop

from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from spotipy import Spotify


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
        self._spotify = spotify
        self.loop = get_running_loop()

    async def async_connect(self) -> dict:
        """Tests the connection and returns the current user profile"""
        profile = await self.loop.run_in_executor(None, self._spotify.me)
        self.name = profile["display_name"]
        return profile

    @staticmethod
    def from_oauth_session(
        session: OAuth2Session,
        country: str = None,
    ) -> "SpotifyAccount":
        """Builds a SpotifyAccount from a Home Assistant OAuth Session"""

        spotify = Spotify(auth=session.token["access_token"])

        return SpotifyAccount(spotify, country=country)
