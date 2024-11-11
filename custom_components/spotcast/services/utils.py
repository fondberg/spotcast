"""Module with utility functions for service calls

Functions:
    - entity_from_target_selector
"""

from typing import Iterable

import voluptuous as vol
from homeassistant.helpers import config_validation as cv


from homeassistant.helpers import entity_registry as er
from homeassistant.core import HomeAssistant

from custom_components.spotcast.services.exceptions import (
    TooManyMediaPlayersError,
    AmbiguousDeviceIdError,
    UnmanagedSelectionError,
    DeviceNotFoundError,
)

EXTRAS_SCHEMA = vol.Schema({
    vol.Optional("position_ms"): cv.positive_int,
    vol.Optional("offset"): cv.positive_int,
    vol.Optional("volume"): vol.All(
        vol.Coerce(int),
        vol.Range(min=0, max=100)
    ),
    vol.Optional("repeat"): vol.In(["track", "context", "off"]),
    vol.Optional("shuffle"): cv.boolean,
})


def entity_from_target_selector(
        hass: HomeAssistant,
        media_players: dict[str, list[str]]
) -> str:
    """Retreives the entity_id to use for the service call from the
    target selector data
    """

    count = 0

    for key, value in media_players.items():
        count += len(value)

    if count > 1:
        raise TooManyMediaPlayersError(
            f"Spotcast service call expect 1 media player, {count} were "
            "provided"
        )

    if "entity_id" in media_players:
        return media_players["entity_id"][0]

    if "device_id" in media_players:
        return entity_from_device_id(hass, media_players["device_id"][0])

    provided_type = list(media_players.keys())[0]
    raise UnmanagedSelectionError(
        f"Spotcast cannot call a service using a {provided_type}"
    )


def entity_from_device_id(
        hass: HomeAssistant,
        device_id: str,
        domain: str = "media_player"
) -> str:
    """Retreives an entity_id from an device id

    Args:
        - hass(HomeAssistant): The Home Assistant Instance
        - device_id(str): the device id used to search the entity_id
        - domain(str, optional): The domain of the entity to find.
            Defaults to `media_player`

    Returns:
        - str: the entity_id
    """
    entity_registry = er.async_get(hass)

    entries = entity_registry.entities.get_entries_for_device_id(device_id)

    current_entry = None
    found = False

    for entry in entries:

        if entry.domain == domain and not found:
            current_entry = entry
            found = True
        elif entry.domain == domain and found:
            raise AmbiguousDeviceIdError(
                f"Device `{device_id}` contains multiple {domain} entities. "
                "Call desired entity directly"
            )

    if current_entry is None:
        raise DeviceNotFoundError(
            f"Could not find a device with valid {domain} for id `{device_id}`"
        )

    return current_entry.entity_id


def clean_extras(extras: dict, keep: Iterable) -> dict:
    """Cleans the extras dictionary before calling the async_play_media

    Args:
        - extras(dict): the dictionary of extras to apply on the
            service call
        - keep(Iterable): a list of extras to keep

    Returns:
        - dict: only the extras request4e
    """
    result = {}

    for key, value in extras.items():

        if key not in keep:
            continue

        result[key] = value

    return result
