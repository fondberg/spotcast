"""Module containing the spotify token class"""

from time import time
from logging import getLogger

from requests import HTTPError
from requests.utils import cookiejar_from_dict
from requests.sessions import Session

from custom_components.spotcast.spotify.exceptions import (
    ExpiredCookiesError,
    InvalidCookiesError,
    UnknownTokenError,
)

LOGGER = getLogger(__name__)


class SpotifyToken:
    """A Spotify Access Token

    Attributes:
        - expires(float): timestamp of when the token will expire

    Methods:
        - is_expired
        - get
        - update

    Constants:
        - USER_AGENT(str)
    """

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/105.0.0.0 Safari/537.36"
    )

    URL = (
        "https://open.spotify.com/get_access_token?reason=transport&"
        "productType=web_player"
    )

    def __init__(
            self,
            access_token: str = None,
            expires: float = None,
            sp_dc: str = None,
            sp_key: str = None,
    ):
        """A Spotify Access Token

        Args:
            - access_token(str): the access token granting Spotify API
                access
            - expires(float): the unix timestamp of the token will
                expire
            - sp_dc(str): a valid sp_dc

        Raises:
            - TypeError: When invalid arguments are provided
        """
        self._access_token = access_token
        self.expires = expires

        # skip if current token is valid
        if not self.is_expired():
            LOGGER.debug("Access Token still valid, skipping refresh")
            return

        if access_token is None:
            LOGGER.debug(
                "Access Token is missing, getting one from Spotify"
            )
        else:
            LOGGER.debug(
                "Access Token is expired. refreshing"
            )

        # raise error if missing sp_dc or sp_key when the other is
        # provided
        if sp_dc is None or sp_key is None:
            raise TypeError(
                "Both sp_dc and sp_key must be provided to refresh_token"
            )

        self.get(sp_dc, sp_key, force=True)

    def is_expired(self) -> bool:
        """Returns True if the token is expired"""

        return (
            self._access_token is None
            or self.expires is None
            or self.expires <= time()
        )

    def get(
            self,
            sp_dc: str,
            sp_key: str,
            force: bool = False
    ) -> str:
        """Gets a valid token for the Spotify API. Refreshing it if
        required.

        args:
            - sp_dc(str): the sp_dc of the account
            - sp_key(str): the sp_key of the account
            - force(bool, optional): If True, forces the token to
                refresh even if not expired. Defaults to False

        Returns:
            - str: the updated token
        """

        if force:
            LOGGER.debug("Refresh of token forced")

        if force or self.is_expired():
            self._access_token, self.expires = self._refresh(
                sp_dc,
                sp_key,
            )

        return self._access_token

    def _refresh(
            self,
            sp_dc: str,
            sp_key: str
    ) -> tuple[str, float]:
        """starts a session to get a new token

        args:
            - sp_dc(str): the sp_dc of the account
            - sp_key(str): the sp_key of the account

        Returns:
            - str: the updated token

        Raises:
            - UnknownTokenError: An error occured while reading the
                response from Spotify
            - ExpiredTokenError: The sp_dc and sp_key are expired
        """

        cookie_dict = {"sp_dc": sp_dc, "sp_key": sp_key}
        headers = {"user-agent": SpotifyToken.USER_AGENT}

        with Session() as session:

            # add cookies
            LOGGER.debug("Adding Cookie to session Cookie Jar")
            cookies = cookiejar_from_dict(cookie_dict)
            session.cookies.update(cookies)

            # make get request to spotify
            LOGGER.debug("Making request to spotify api for new token")
            response = session.get(
                SpotifyToken.URL,
                headers=headers
            )

            try:
                response.raise_for_status()
            except HTTPError as exc:

                LOGGER.debug("%s: %s", response.status_code, response.text)

                if response.status_code == 401:
                    raise InvalidCookiesError(
                        "The sp_dc and sp_key provided are invalid"
                    ) from exc

                raise UnknownTokenError(
                    "Couldn't retrieve Spotify Token"
                ) from exc

            config = response.json()

        try:
            access_token = config["accessToken"]
            expires = config["accessTokenExpirationTimestampMs"]
        except KeyError as exc:
            raise UnknownTokenError(
                "Response from Spotify is unexpected"
            ) from exc

        expires = expires / 1000

        LOGGER.debug("Token and expiration retrieved successfully")

        return access_token, expires
