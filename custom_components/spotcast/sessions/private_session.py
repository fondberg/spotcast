"""Module containing the InternalSession class that manages the
internal api credentials

Classes:
    - PrivateSession
    - ExpiredSpotifyKeyError
    - TokenError
"""

from time import time
from asyncio import Lock
from random import randrange
from aiohttp import ClientSession
from aiohttp.client_exceptions import (
    ContentTypeError,
    ClientOSError,
    ClientResponseError,
)
from types import MappingProxyType
from logging import getLogger
import json

from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import (
    CLOCK_OUT_OF_SYNC_MAX_SEC,
)
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.crypto import spotify_totp
from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession,
)
from custom_components.spotcast.sessions.retry_supervisor import (
    RetrySupervisor,
)
from custom_components.spotcast.sessions.exceptions import (
    TokenRefreshError,
    ExpiredSpotifyCookiesError,
    InternalServerError,
    UpstreamServerNotready,
)
from custom_components.spotcast.utils import is_valid_json

LOGGER = getLogger(__name__)


class PrivateSession(ConnectionSession):
    """Api session with access to Spotify's private API

    Attributes:
        - hass(HomeAssistant): The Home Assistant Instance
        - entry(ConfigEntry): Configuration entry of a Spotify Account

    Properties:
        - token(str): the current access token of the session
        - valid_token(bool): True if the token is currently valid
        - cookies(dict[str,str]): the cookie dictionary to include in
            the api request

    Constants:
        - HEADERS(dict): dictionary of headers to include in all API
            call.
        - REQUEST_URL(str): the url where to make an authentication
            request
        - EXPIRED_LOCATION(str): The location header value when an
            authentication request fails
        - TOKEN_KEY(str): the key containing the access token in the
            api response
        - EXPIRATION_KEY(str): the key containing the expires_at of
            the token in the api response

    Methods:
        - async_ensure_token_valid
        - async_refresh_tokne
    """

    HEADERS = MappingProxyType({
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) "
            "Gecko/20100101 "
            "Firefox/136.0"
        ),
        "Accept": "application/json",
    })

    BASE_URL = "https://open.spotify.com"
    TOKEN_ENDPOINT = "get_access_token"
    SERVER_TIME_ENDPOINT = "server-time"

    REQUEST_URL = (
        "https://open.spotify.com/get_access_token?"
        "reason=transport&productType=web_player"
    )

    EXPIRED_LOCATION = (
        "/get_access_token?"
        "reason=transport&productType=web_player&_authfailed=1"
    )

    TOKEN_KEY = "accessToken"
    TOKEN_LENGTH = 362
    EXPIRATION_KEY = "accessTokenExpirationTimestampMs"
    API_ENDPOINT = "https://spclient.wg.spotify.com"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Api session with access to Spotify's private API

        Args:
            - hass(HomeAssistant): The Home Assistant Instance
            - entry(ConfigEntry): Configuration entry of a Spotify
                Account
        """
        self._access_token = None
        self._expires_at = 0
        self._totp = spotify_totp.get_totp()

        super().__init__(hass, entry)

    @property
    def token(self) -> str:
        """Returns the token"""
        return self._access_token

    @property
    def clean_token(self) -> str:
        """Returns the token"""
        return self.token

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
        return {
            "sp_dc": sp_dc,
            "sp_key": sp_key,
        }

    @property
    def headers(self) -> dict:
        """Returns the headers to user in the token refresh process"""
        return {
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_"
                f"{randrange(11, 15)}_{randrange(4, 9)}) AppleWebKit/"
                f"{randrange(530, 537)}.{randrange(30, 37)} (KHTML, like "
                f"Gecko) Chrome/{randrange(80, 105)}.0.{randrange(3000, 4500)}"
                f".{randrange(60, 125)} Safari/{randrange(530, 537)}"
                f".{randrange(30, 36)}"
            ),
            "Accept": "application/json",
        }

    async def async_ensure_token_valid(self) -> bool:
        """Ensure the current token is valid or gets a new one. Returns
        True if the refcresh worked or False if it didn't
        """

        not_ready = False

        async with self._token_lock:

            if not self.supervisor.is_ready:
                not_ready = True

            elif self.valid_token:
                return

            else:

                LOGGER.debug("Token is expired. Getting a new one")

                try:
                    await self.async_refresh_token()
                    self.supervisor._is_healthy = True
                except self.supervisor.SUPERVISED_EXCEPTIONS as exc:
                    self.supervisor._is_healthy = False
                    self.supervisor.log_message(exc)
                    not_ready = True

        if not_ready:
            raise UpstreamServerNotready("Server not ready for refresh")

    def _endpoint(self, endpoint: str) -> str:
        """Returns a spotify API endpoint"""
        return f"{self.BASE_URL}/{endpoint}"

    async def async_refresh_token(
        self,
        max_retries: int = 5
    ) -> tuple[str, float]:
        """Retrives a new token, sets it in the session and returns
        the token and when it expires

        Args:
            - max_retries(int, optional): the maximum number of retries
                before raising an error

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

            # get server time
            async with session.get(
                url=self._endpoint(self.SERVER_TIME_ENDPOINT),
                headers=self.headers
            ) as response:
                data = await response.json()
                self.raise_for_status(
                    response.status,
                    json.dumps(data),
                    response.headers,
                )
                server_time = data["serverTime"]

            totp_value = self._totp.at(server_time)

            retry_count = 0

            while True:

                async with session.get(
                        url=self._endpoint(self.TOKEN_ENDPOINT),
                        allow_redirects=False,
                        headers=self.headers,
                        params={
                            "reason": "transport",
                            "productType": "web-player",
                            "totp": totp_value,
                            "totpServer": totp_value,
                            "totpVer": 5,
                            "sTime": server_time,
                            "cTime": server_time,
                        },
                ) as response:
                    data = await response.text()
                    headers = response.headers
                    status = response.status

                try:
                    self.raise_for_status(status, data, headers)
                    self._test_token(
                        token=json.loads(data).get(self.TOKEN_KEY, ""),
                    )
                    break
                except TokenRefreshError as exc:
                    if retry_count >= max_retries - 1:
                        raise exc
                    retry_count += 1

            data = json.loads(data)

            self._access_token = data[self.TOKEN_KEY]
            self._expires_at = int(data[self.EXPIRATION_KEY]) // 1000
            self._is_healthy = True
            self.supervisor.is_healthy = True

            return {
                "access_token": self._access_token,
                "expires_at": self._expires_at
            }

    def raise_for_status(self, status: int, content: str, headers: dict):
        """Raises an error for error statuses. Otherwise returns

        Raises:
            InternalServerError: Raised when the Spotify server is
                experiencing issues
            ExpiredSpotifyCookiesError: Raised when the sp_dc and
                sp_key are expired
            TokenRefreshError: Raised when a client error is raised
        """

        if (500 <= status < 600) or status == 104:
            raise InternalServerError(status, content)

        if status == 302 and headers.get("Location") == self.EXPIRED_LOCATION:
            LOGGER.error(
                "Unsuccessful token request. Location header %s. "
                "sp_dc and sp_key are likely expired",
                self.EXPIRED_LOCATION,
            )
            self._is_healthy = False
            raise ExpiredSpotifyCookiesError("Expired sp_dc, sp_key")

        if (
                not is_valid_json(content)
                or (400 <= status < 500)
        ):
            self._is_healthy = False
            raise TokenRefreshError(content)

    async def _test_token(self, token: str):
        """Test the token and returns if valid. Otherwise raises a
        TokenRefreshError. Must be call only with fresh token"""

        headers = self.headers
        headers |= {"Authorization": f"Bearer {token}"}

        async with ClientSession(cookies=self.cookies) as session:

            # get server time
            async with session.get(
                url="https://api.spotify.com/v1/me",
                headers=headers
            ) as response:
                await response.json()

        if not response.ok:
            LOGGER.debug("Token received is not valid. Retrying")
            raise TokenRefreshError("Token received is not valid. Retrying")
