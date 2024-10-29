"""Module containing the InternalSession class that manages the
internal api credentials"""

from time import time
from asyncio import Lock
from aiohttp import ClientSession, ClientResponseError, ContentTypeError
from types import MappingProxyType
from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.config_entry_oauth2_flow import (
    CLOCK_OUT_OF_SYNC_MAX_SEC,
)
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
)

LOGGER = getLogger(__name__)

HEADERS = MappingProxyType({
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
        "Safari/537.36"
    )
})

REQUEST_URL = (
    "https://open.spotify.com/get_access_token?"
    "reason=transport&productType=web_player"
)

EXPIRED_LOCATION = (
    "/get_access_token?reason=transport&productType=web_player&_authfailed=1"
)

TOKEN_KEY = "accessToken"
EXPIRATION_KEY = "accessTokenExpirationTimestampMs"


class InternalSession(ConnectionSession):

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._access_token = None
        self._expires_at = 0
        self._token_lock = Lock()

    @property
    def token(self) -> str:
        """Returns the token"""
        return self._access_token

    @property
    def valid_token(self) -> bool:
        """Returns True if the token is still valid"""
        return self._expires_at > time() + CLOCK_OUT_OF_SYNC_MAX_SEC

    @property
    def cookies(self) -> dict[str, str]:
        """The cookie dictionary with the sp_dc and sp_key"""
        internal_api = self.entry.data["internal_api"]
        sp_dc = internal_api["sp_dc"]
        sp_key = internal_api["sp_key"]
        return {"sp_dc": sp_dc, "sp_key": sp_key}

    async def async_ensure_token_valid(self) -> None:
        """Ensure the current token is valid or gets a new one"""
        async with self._token_lock:
            if self.valid_token:
                return

            LOGGER.debug("Token is expired. Getting a new one")

            await self.async_refresh_token()

    async def async_refresh_token(self) -> tuple[str, float]:
        """Retrives a new token, sets it in the session and returns
        the token and when it expires

        Returns:
            - tuple[str, int]: the token and a timestamp of when it
                expires

        Raises:
            - ExpiredSpotifyKeyError: Raised if the sp_dc and sp_key
                are expired
            - TokenError: raised if an error occured when getting the
                token
        """

        async with ClientSession(cookies=self.cookies) as session:
            async with session.get(
                REQUEST_URL,
                allow_redirects=False,
                headers=HEADERS
            ) as response:

                location = response.headers.get("Location")

                if response.status == 302 and location == EXPIRED_LOCATION:
                    LOGGER.error(
                        "Unsuccessful token request. Location header %s. "
                        "sp_dc and sp_key are likely expired",
                        location
                    )
                    raise ExpiredSpotifyKeyError("Expired sp_dc, sp_key")

                try:
                    data = await response.json()
                except ContentTypeError as exc:
                    error_message = await response.text()
                    raise TokenError(error_message) from exc

                if not response.ok:
                    raise TokenError(
                        f"{response.status}: {data}"
                    )

            self._access_token = data[TOKEN_KEY]
            self._expires_at = int(data[EXPIRATION_KEY]) // 1000

            return {
                "access_token": self._access_token,
                "expires_at": self._expires_at
            }


class ExpiredSpotifyKeyError(HomeAssistantError):
    """Raised if the sp_dc and sp_key are expired"""


class TokenError(HomeAssistantError):
    """Raised when there is an error getting the token from spotify"""
