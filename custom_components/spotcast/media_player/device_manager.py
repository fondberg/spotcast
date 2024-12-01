"""Module for the DeviceManager that takes care of managing new
devices and unavailable ones

Classes:
    - DeviceManager
"""

from logging import getLogger

from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.media_player import (
    SpotifyDevice,
)
from custom_components.spotcast.spotify import SpotifyAccount


LOGGER = getLogger(__name__)


class DeviceManager:
    """Entity that manages Spotify Devices as they become available
    and drop from the device list

    Attributes:
        - tracked_devices(dict[str, SpotifyDevice]): A dictionary of
            all the currently tracked devices for the account. The Key
            being the id of the device

    Constants:
        - IGNORE_DEVICE_TYPES(tuple[str]): A list of device type to
            ignore when creating new media_players

    Methods:
        - async_update
    """
    IGNORE_DEVICE_TYPES = (
        "CastAudio",
    )

    def __init__(
        self,
        account: SpotifyAccount,
        async_add_entitites: AddEntitiesCallback,
    ):

        self.tracked_devices: dict[str, SpotifyDevice] = {}
        self.unavailable_devices: dict[str, SpotifyDevice] = {}

        self._account = account
        self.async_add_entities = async_add_entitites

    async def async_update(self, _=None):

        current_devices = await self._account.async_devices()
        current_devices = {x["id"]: x for x in current_devices}

        for id, device in current_devices.items():

            if device["type"] in self.IGNORE_DEVICE_TYPES:
                LOGGER.debug(
                    "Ignoring player `%s` of type `%s`",
                    device["name"],
                    device["type"],
                )
                continue

            if (
                id not in self.tracked_devices
                and id in self.unavailable_devices
            ):
                LOGGER.info(
                    "Device `%s` has became available again for account `%s`",
                    device["name"],
                    self._account.name,
                )
                self.tracked_devices[id] = self.unavailable_devices.pop(id)
                self.tracked_devices[id]._is_unavailable = False

            elif (
                id not in self.tracked_devices
                and id not in self.unavailable_devices
            ):
                LOGGER.info(
                    "Adding New Device `%s` for account `%s`",
                    device["name"],
                    self._account.name,
                )
                new_device = SpotifyDevice(self._account, device)
                self.tracked_devices[id] = new_device
                self.async_add_entities([new_device])

        playback_state = await self._account.async_playback_state()
        playing_id = None
        remove = []

        if "device" in playback_state:
            playing_id = playback_state["device"]["id"]

        for id, device in self.tracked_devices.items():
            if id not in current_devices:
                LOGGER.info(
                    "Marking device `%s` unavailable for account `%s`",
                    device.name,
                    self._account.name
                )
                remove.append(id)
                entity = self.tracked_devices[id]
                entity._is_unavailable = True
            else:
                LOGGER.debug("Updating device info for `%s`", device.name)
                device._device_data = current_devices[id]

                if device.id == playing_id:
                    LOGGER.debug("Feeding playback state to `%s`", device.name)
                    device._playback_state = playback_state
                else:
                    device._playback_state = {}

        for id in remove:
            self.unavailable_devices[id] = self.tracked_devices.pop(id)
