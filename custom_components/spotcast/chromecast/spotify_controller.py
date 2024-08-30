"""Module containing the Spotify App Controller for chromecast devices
"""

from logging import getLogger

from pychromecast.controllers import BaseController
from pychromecast import Chromecast

LOGGER = getLogger(__name__)


class SpotifyController(BaseController):
    """A Chromcast controller for interacting with Spotify

    Attributes:
        - ...

    Constants:
        - APP_CODE(str): the chromecast app code for spotify 
        - APP_NAME(str): the chromecast namespace for spotify 
    """

    APP_CODE = "CC32E753"
    APP_NAMESPACE = "urn:x-cast:com.spotify.chromecast.secure.v1"

    def __init__(
            self,
            access_token: str = None,
            expires: float = None,
    ):
        """A Chromecast controller for interactinf with spotify

        Args:
            - access_token(str, optional): the toek used for connecting
                to the Spotify App. Is retrived automatically if not
                provided. Defaults to None.
            - expires(int, optional): the timestamp of when the token
                expires. Is updated when a new token is retrived.
                Defaults to None
        """
        super(SpotifyController, self).__init__(
            self.APP_CODE,
            self.APP_NAMESPACE
        )

        self.access_token = access_token
        self.expires = expires
