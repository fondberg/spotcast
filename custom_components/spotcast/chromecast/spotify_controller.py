"""Module containing the Spotify App Controller for chromecast devices
"""

from logging import getLogger
import threading

from pychromecast.controllers import BaseController
from pychromecast.controllers import CastMessage
from requests import post, Response

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.chromecast import ChromecastDevice

LOGGER = getLogger(__name__)


class SpotifyController(BaseController):
    """A Chromcast controller for interacting with Spotify

    Attributes:
        - account(SpotifyAccount): The spotify account in charge of the
            spotify controller

    Constants:
        - APP_CODE(str): the chromecast app code for spotify
        - APP_NAME(str): the chromecast namespace for spotify
        - APP_HOSTNAME(str): the hostname for the spotify API
        - TYPE_GET_INFO(str): mesage type to get info
        - TYPE_GET_INFO_RESPONSE(str): message type for the response to
            get info
        - TYPE_ADD_USER(str): message type to add a user
        - TYPE_ADD_USER_RESPONSE(str): message type for the response to
            add user
        - TYPE_ADD_USER_ERROR(str): message type for add user error
    """

    APP_CODE = "CC32E753"
    APP_NAMESPACE = "urn:x-cast:com.spotify.chromecast.secure.v1"
    APP_HOSTNAME = "spclient.wg.spotify.com"

    TYPE_GET_INFO = "getInfo"
    TYPE_GET_INFO_RESPONSE = "getInfoResponse"
    TYPE_ADD_USER = "addUser"
    TYPE_ADD_USER_RESPONSE = "addUserResponse"
    TYPE_ADD_USER_ERROR = "addUserError"

    def __init__(
            self,
            account: SpotifyAccount,
            device: ChromecastDevice,
    ):
        """A Chromecast controller for interacting with spotify

        Args:
            - account(SpotifyAccount): The account in charge of the
                spotify controller
            - device(ChromecastDevice): The device managed by the
                controller
        """
        super(SpotifyController, self).__init__(
            self.APP_CODE,
            self.APP_NAMESPACE
        )

        self.account = account
        self.device = device
        self.waiting = threading.Event()

    def receive_message(self, _message: CastMessage, _data: dict) -> bool:
        """Called when a message is received that matches the namespace.
        Returns boolean indicating if message was handled.
        data is message.payload_utf8 interpreted as a JSON dict.
        """

        message_type = _data["type"]

        if message_type == SpotifyController.TYPE_GET_INFO_RESPONSE:
            return self._get_info_response_handler(_message, _data)

        if message_type == SpotifyController.TYPE_ADD_USER_RESPONSE:
            return self._add_user_response_handler(_message, _data)

        if message_type == SpotifyController.TYPE_ADD_USER_ERROR:
            return self._add_user_error_handler(_message, _data)

    def _get_info_response_handler(
            self,
            message: CastMessage,
            data: dict
    ) -> bool:
        """Handler for the get info response message"""

        headers = {
            "authority": SpotifyController.APP_HOSTNAME,
            "authorization": f"Bearer {self.account.get_token()}",
            "content-type": "text/plain;charset=UTF-8",
        }

        body = {
            "clientId": data["payload"]["clientId"],
            "deviceId": self.device.spotify_device_id(),
        }

        response: Response = post(
            url=(
                f"https://{SpotifyController.APP_HOSTNAME}/device-auth/v2"
                "/refresh"
            ),
            headers=headers,
            data=body,
        ),

        content = response.json()

        self.send_message({
            "type": SpotifyController.TYPE_ADD_USER,
            "payload": {
                "blob": content["accessToken"],
                "tokenType": "accessToken"
            },
        })

        return True

    def _add_user_response_handler(
            self,
            message: CastMessage,
            data: dict
    ) -> bool:
        """Handler for the add user response message"""
        self.is_launched = True
        self.waiting.set()

        return True

    def _add_user_error_handler(
            self,
            message: CastMessage,
            data: dict
    ) -> bool:
        """Handler for the add user error message"""
        self.device = None
        self.credential_error = True
        self.waiting.set()

        return True
