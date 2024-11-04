"""Module to manage types of media_player compatible with spotcast

Classes:
    - Chromecast
"""
from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast,
)
from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer
)
from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice
)

from custom_components.spotcast.spotify import SpotifyAccount

LOGGER = getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    account = await SpotifyAccount.async_from_config_entry(hass, entry)

    media_players = []

    devices = await account.async_devices()

    for device in devices:
        LOGGER.debug("Creating Media Player for %s", device["name"])

        media_players.append(SpotifyDevice(account, device))

    async_add_entities(
        media_players,
        True,
    )
