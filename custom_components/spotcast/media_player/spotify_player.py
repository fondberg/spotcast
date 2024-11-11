"""Module the SpotifyDevice media player

Classes:
    - SpotifyDevice
"""

from logging import getLogger

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.const import (
    STATE_ON,
    STATE_OFF,
    STATE_UNAVAILABLE
)

from custom_components.spotcast.media_player import MediaPlayer
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast import DOMAIN

LOGGER = getLogger(__name__)


class SpotifyDevice(MediaPlayer, MediaPlayerEntity):
    """Representation of a device in spotify

    Attributes:
        - entity_id(str): Entity Id of the device in Home Assistant
        - device_info(DeviceInfo): the device information linked to the
            media player

    Properties:
        - unique_id(str): the unique identifier for Home Assistant
        - id(str): the spotify device id in spotify for the device
        - name(str): the name as reported by Spotify
        - icon(str): the icon of the device based on the state
        - state(str): the current state of the device

    Methods:
        - async_update
    """

    INTEGRATION = DOMAIN

    def __init__(self, account: SpotifyAccount, device_data: dict):
        """Initialize the spotify device

        Args:
            - account(SpotifyAccount): the account the device is linked
                to.
            - device_data(dict): the information related to device
                provided by the Spotify API
        """
        self._device_data: dict = device_data
        self._account: SpotifyAccount = account
        self.entity_id = self._define_entity_id()
        self._is_unavailable = False

        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, self.id)},
            manufacturer="Spotify AB",
            model=f"Spotify Connect {self._device_data['type']}",
            name=f"Spotcast - {self.name} ({self._account.name})",
        )

    @property
    def unique_id(self) -> str:
        """The unique identifier for Home Assistant"""
        return f"{self.id}_{self._account.id}_spotcast_device"

    @property
    def id(self) -> str:
        """The Spotify Device id from the API"""
        return self._device_data["id"]

    @property
    def name(self):
        """The name of the device as reported by Spotify"""
        name = self._device_data["name"]
        return f"Spotcast ({self._account.name}) - {name}"

    @property
    def icon(self):
        """The icon to show in Home Assistant based on the state"""

        icon_map = {
            "Computer": "mdi:laptop",
            "Smartphone": "mdi:smartphone",
            "*": "mdi:speaker"
        }

        try:
            icon = icon_map[self._device_data["type"]]
        except KeyError:
            icon = icon_map["*"]

        if self.state == STATE_OFF:
            icon += "-off"

        return icon

    @property
    def state(self):
        """The current state of the player"""

        if self._is_unavailable:
            return STATE_UNAVAILABLE

        is_active = self._device_data["is_active"]

        return STATE_ON if is_active else STATE_OFF

    def _define_entity_id(self):
        """Define the entity ID based on the account profile"""

        removals = "()"

        name: str = self._device_data["name"]

        name = name.lower()
        name = name.replace(" ", "_")

        for char in removals:
            name = name.replace(char, "")

        return f"media_player.{name}_{self._account.id}_spotcast"
