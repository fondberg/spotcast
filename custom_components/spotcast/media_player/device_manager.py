"""Module for the DeviceManager that takes care of managing new
devices and unavailable ones"""

from logging import getLogger

from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.media_player import (
    SpotifyDevice,
    SpotifyAccount,
)

LOGGER = getLogger(__name__)

IGNORE_DEVICE_TYPES = (
    "CastAudio",
)


class DeviceManager:

    def __init__(
            self,
            devices: list[SpotifyDevice],
            account: SpotifyAccount,
            async_add_entitites: AddEntitiesCallback,
    ):
        self.tracked_devices: dict[str, SpotifyDevice] = {
            x.id: x for x in devices
        }
        self._account = account
        self.async_add_entities = async_add_entitites

    async def async_update(self):

        current_devices = await self._account.async_devices()
        current_devices = {x.id: x for x in current_devices}

        for id, device in current_devices.items():

            if device["type"] in IGNORE_DEVICE_TYPES:
                LOGGER.debug(
                    "Ignoring player `%s` of type `%s`",
                    device["name"],
                    device["type"],
                )
                continue

            if id not in self.tracked_devices:
                new_device = SpotifyDevice(self._account, device)
                self.tracked_devices[id] = new_device
                self.async_add_entities([new_device])

        for id, device in self.tracked_devices.items():
            entity = self.tracked_devices.pop(id)
            entity._is_unavailable = True
