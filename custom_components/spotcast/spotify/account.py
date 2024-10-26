"""Module for the spotify account class"""

from logging import getLogger

from spotipy import Spotify

from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
    ConnectionSession,
)

LOGGER = getLogger(__name__)


class SpotifyAccount:

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
            external_session: OAuth2Session,
            internal_session: InternalSession,
            country: str = None,
    ):
        self.sessions: dict[str, ConnectionSession] = {
            "external": external_session,
            "internal": internal_session,
        }

        self._spotify = Spotify(auth=self.sessions["external"].token)

        self.country = country
        self.name = None

    async def async_get_token(self, api: str) -> str:
        """Retrives a token from the requested session.

        Args:
            - api(str): The api to retrive from. Can be `internal` or
                `external`.
        """
        await self.sessions[api].async_ensure_token_valid()
        return self.sessions[api].token

    async def async_ensure_tokens_valid(self):
        """Ensures the token are valid"""
        for key, session in self.sessions.items():
            LOGGER.debug("Refreshing %s api token", key)
            session.async_ensure_token_valid()
            LOGGER.debug("Done refreshing %s api token", key)

    async def async_profile(self) -> dict:
        """Test the connection and returns a user profile"""
        LOGGER.debug("Getting Profile from Spotify")
        profile = self._spotify.me()

        name = profile["id"] if "id" in profile else profile["display_name"]

        LOGGER.debug("Profile retrived for user %s", name)
        self.name = name
        return profile

    async def async_devices(self) -> list[dict]:
        """Returns the list of devices"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Devices for account `%s`", self.name)
        devices = self._spotify.devices()["devices"]

        # Log all the devices found
        for device in devices:
            LOGGER.debug("Found Device [%s](%s)", device["name"], device["id"])

        return devices
