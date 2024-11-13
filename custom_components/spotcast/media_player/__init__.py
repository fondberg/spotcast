"""Module to manage types of media_player compatible with spotcast

Classes:
    - Chromecast
    - SpotifyDevice
    - MediaPlayer
    - DeviceManager

Functions:
    - async_setup_entry
"""
from logging import getLogger
import datetime as dt

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from custom_components.spotcast.utils import ensure_default_data
from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast,
)
from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer
)
from custom_components.spotcast.media_player.spotify_player import (
    SpotifyDevice
)
from custom_components.spotcast.media_player.device_manager import (
    DeviceManager
)
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.const import DOMAIN

LOGGER = getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    account = await SpotifyAccount.async_from_config_entry(hass, entry)
    device_manager = DeviceManager(account, async_add_entities)

    await device_manager.async_update()

    device_listener = async_track_time_interval(
        hass,
        device_manager.async_update,
        dt.timedelta(seconds=30)
    )

    hass = ensure_default_data(hass, entry.entry_id)

    domain_data = hass.data[DOMAIN]
    domain_data[entry.entry_id]["device_listener"] = device_listener
