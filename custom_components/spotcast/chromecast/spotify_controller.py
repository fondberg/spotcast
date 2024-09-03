"""Module containing the Spotify App Controller for chromecast devices
"""

from logging import getLogger
import threading
import json

from pychromecast.controllers import BaseController
from pychromecast.controllers import CastMessage
from requests import post, Response, HTTPError

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast
)

from custom_components.spotcast.chromecast.exceptions import AppLaunchError

LOGGER = getLogger(__name__)


class SpotifyController(BaseController):
    """A Chromcast controller for interacting with Spotify

    Attributes:
        - account(SpotifyAccount): The spotify account in charge of the
            spotify controller

    Constants:
        - APP_ID(str): the chromecast app code for spotify
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

    APP_ID = "CC32E753"
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
    ):
        """A Chromecast controller for interacting with spotify

        Args:
            - account(SpotifyAccount): The account in charge of the
                spotify controller
            - device(ChromecastDevice): The device managed by the
                controller
        """
        super(SpotifyController, self).__init__(
            self.APP_NAMESPACE,
            self.APP_ID
        )

        self.account = account
        self.waiting = threading.Event()
        self.is_launched = False

    def launch_app(self, device: Chromecast, max_attempts=10):
        """Launches the spotify app"""

        def callback(*_):
            self.send_message({
                "type": self.TYPE_GET_INFO,
                "payload": {
                    "remoteName": device.name,
                    "deviceID": device.id(),
                    "deviceAPI_isGroup": False,
                }
            })

        device.start_app(self.APP_ID)
        device.wait()

        self.waiting.clear()

        LOGGER.debug("Requesting Spotify App to launch on `%s`", device.name)
        self.launch(callback_function=callback)

        counter = 0

        while True:

            if self.is_launched:
                LOGGER.debug(
                    "Spotify App Launched successfully on `%s`",
                    device.name,
                )
                break

            if max_attempts is not None and counter >= max_attempts:
                raise AppLaunchError(
                    "Timeout when waiting for status response from Spotify app"
                )

            LOGGER.debug(
                "Spotify App not yet launched on `%s`. Waiting Before retry",
                device.name,
            )
            self.waiting.wait(1)
            counter += 1

        devices = self.account._spotify.devices()
        foo = "bar"

    def receive_message(self, _message: CastMessage, data: dict) -> bool:
        """Called when a message is received that matches the namespace.
        Returns boolean indicating if message was handled.
        data is message.payload_utf8 interpreted as a JSON dict.
        """

        message_type = data["type"]

        LOGGER.debug("Received message of type `%s`", message_type)

        if message_type == SpotifyController.TYPE_GET_INFO_RESPONSE:
            return self._get_info_response_handler(_message, data)

        if message_type == SpotifyController.TYPE_ADD_USER_RESPONSE:
            return self._add_user_response_handler(_message, data)

        if message_type == SpotifyController.TYPE_ADD_USER_ERROR:
            return self._add_user_error_handler(_message, data)

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
            "clientId": data["payload"]["clientID"],
            "deviceId": data["payload"]["deviceID"],
        }

        response: Response = post(
            url=(
                f"https://{SpotifyController.APP_HOSTNAME}/device-auth/v1"
                "/refresh"
            ),
            headers=headers,
            data=json.dumps(body),
        )

        try:
            response.raise_for_status()
        except HTTPError as exc:
            raise AppLaunchError(
                f"{response.status_code}: {response.reason}"
            ) from exc

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
