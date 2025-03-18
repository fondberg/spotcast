"""Module containing the InternalSession class that manages the
internal api credentials

Classes:
    - PrivateSession
    - ExpiredSpotifyKeyError
    - TokenError
"""

from time import time
from asyncio import Lock
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError, ClientOSError
from types import MappingProxyType
from logging import getLogger

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
        "Accept": "*/*",
        "Accept-Encoding": "gzip, defalte, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "baggage": (
            "sentry-environment=production,"
            "sentry-release=web-player_2025-03-17_1742227223106_b68bcd7,"
            "sentry-public_key=de32132fc06e4b28965ecf25332c3a25,"
            "sentry-trace_id=e0d6b0af78cf44cb94453ce3bec73054,"
            "sentry-sample_rate=0.008,"
            "sentry-sampled=false"
        )
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
            "sp_t": "344a4884-e69f-4115-8110-509d621352b8",
            "sp_adid": "b48835ed-dda5-457f-8795-7a26eb62aeed",
            "sp_gaid": "bb0992a5-99db-4b98-9de6-e1fb9a1174b5",
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

            # get server time
            async with session.get(
                url=self._endpoint(self.SERVER_TIME_ENDPOINT),
                headers=self.HEADERS
            ) as response:
                data = await response.json()
                server_time = data["serverTime"]

            totp_value = self._totp.at(server_time)

            async with session.get(
                    url=self._endpoint(self.TOKEN_ENDPOINT),
                    allow_redirects=False,
                    headers=self.HEADERS,
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

                location = response.headers.get("Location")

                if (
                        response.status == 302
                        and location == self.EXPIRED_LOCATION
                ):
                    LOGGER.error(
                        "Unsuccessful token request. Location header %s. "
                        "sp_dc and sp_key are likely expired",
                        location
                    )
                    self._is_healthy = False
                    raise ExpiredSpotifyCookiesError("Expired sp_dc, sp_key")

                if (
                        (response.status >= 500 and response.status < 600)
                        or (response.status == 104)
                ):
                    raise InternalServerError(
                        response.status,
                        await response.text()
                    )

                try:
                    data = await response.json()
                except ContentTypeError as exc:
                    self._is_healthy = False
                    error_message = await response.text()
                    raise TokenRefreshError(error_message) from exc

                if not response.ok:
                    self._is_healthy = False
                    raise TokenRefreshError(
                        f"{response.status}: {data}"
                    )

            self._access_token = data[self.TOKEN_KEY]
            self._expires_at = int(data[self.EXPIRATION_KEY]) // 1000
            self._is_healthy = True
            self.supervisor.is_healthy = True

            return {
                "access_token": self._access_token,
                "expires_at": self._expires_at
            }
