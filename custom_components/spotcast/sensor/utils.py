"""Utility functions for the sensor creation

Utils:
    - device_from_account
"""

from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from custom_components.spotcast import SpotifyAccount, DOMAIN


def device_from_account(account: SpotifyAccount):

    return DeviceInfo(
        identifiers={(DOMAIN, account.id)},
        manufacturer="Spotify AB",
        model=f"Spotify {account.profile['product']}",
        name=f"Spotcast {account.name}",
        entry_type=DeviceEntryType.SERVICE,
        configuration_url="https://open.spotify.com",
    )
