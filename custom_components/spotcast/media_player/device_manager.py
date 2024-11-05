"""Module for the DeviceManager that takes care of managing new
devices and unavailable ones"""

from logging import getLogger

from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.media_player import (
    SpotifyDevice,
)
from custom_components.spotcast.spotify import SpotifyAccount

LOGGER = getLogger(__name__)

IGNORE_DEVICE_TYPES = (
    "CastAudio",
)


class DeviceManager:

    def __init__(
        self,
        account: SpotifyAccount,
        async_add_entitites: AddEntitiesCallback,
    ):

        self.tracked_devices: dict[str, SpotifyDevice] = {}

        self._account = account
        self.async_add_entities = async_add_entitites

    async def async_update(self, _=None):

        current_devices = await self._account.async_devices()
        current_devices = {x["id"]: x for x in current_devices}

        for id, device in current_devices.items():

            if device["type"] in IGNORE_DEVICE_TYPES:
                LOGGER.debug(
                    "Ignoring player `%s` of type `%s`",
                    device["name"],
                    device["type"],
                )
                continue

            if id not in self.tracked_devices:
                LOGGER.info(
                    "Adding New Device `%s` for account `%s`",
                    device["name"],
                    self._account.name,
                )
                new_device = SpotifyDevice(self._account, device)
                self.tracked_devices[id] = new_device
                self.async_add_entities([new_device])

        remove = []

        for id, device in self.tracked_devices.items():
            if id not in current_devices:
                LOGGER.info(
                    "Marking device `%s` unavailable for account `%s`",
                    device.name,
                    self._account.name
                )
                entity = self.tracked_devices["id"]
                entity._is_unavailable = True

        for id in remove:
            self.tracked_devices.pop(id)
