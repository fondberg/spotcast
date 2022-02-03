"""Sensor platform for Chromecast devices."""
from __future__ import annotations

import collections
import json
import logging
from datetime import timedelta
import homeassistant.core as ha_core

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_OK, STATE_UNKNOWN
from homeassistant.util import dt

from .helpers import get_cast_devices
from .const import (
    DOMAIN,
    CONF_SPOTIFY_COUNTRY
)

_LOGGER = logging.getLogger(__name__)

SENSOR_SCAN_INTERVAL_SECS = 60
SCAN_INTERVAL = timedelta(seconds=SENSOR_SCAN_INTERVAL_SECS)


def setup_platform(hass:ha_core.HomeAssistant, config:collections.OrderedDict, add_devices, discovery_info=None):

    try:
        country = config[CONF_SPOTIFY_COUNTRY]
    except KeyError:
        country = None

    add_devices([ChromecastDevicesSensor(hass)])
    add_devices([ChromecastPlaylistSensor(hass, country)])


class ChromecastDevicesSensor(SensorEntity):
    def __init__(self, hass):
        self.hass = hass
        self._state = STATE_UNKNOWN
        self._chromecast_devices = []
        self._attributes = {"devices_json": [], "devices": [], "last_update": None}
        _LOGGER.debug("initiating sensor")

    @property
    def name(self):
        return "Chromecast Devices"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        _LOGGER.debug("Getting chromecast devices")

        known_devices = get_cast_devices(self.hass)
        _LOGGER.debug("sensor devices %s", known_devices)

        chromecasts = [
            {
                "uuid": str(cast_info.cast_info.uuid),
                "model_name": cast_info.cast_info.model_name,
                "name": cast_info.cast_info.friendly_name,
                "manufacturer": cast_info.cast_info.manufacturer,
                "cast_type": cast_info.cast_info.cast_type,
            }
            for cast_info in known_devices
        ]

        self._attributes["devices_json"] = json.dumps(chromecasts, ensure_ascii=False)
        self._attributes["devices"] = chromecasts
        self._attributes["last_update"] = dt.now().isoformat("T")
        self._state = STATE_OK


class ChromecastPlaylistSensor(SensorEntity):
    def __init__(self, hass: ha_core, country=None):
        self.hass = hass
        self._state = STATE_UNKNOWN
        self.country = country
        self._attributes = {"playlists": [], "last_update": None}
        _LOGGER.debug("initiating playlist sensor")

    @property
    def name(self):
        return "Playlists sensor"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        _LOGGER.debug("Getting playlists")

        if self.country is not None:
            country_code = self.country
        else:
            # kept the country code to SE if not provided by the user for retrocompatibility
            country_code = "SE"

        playlist_type = "user"
        locale = "en"
        limit = 10
        account = None

        resp = self.hass.data[DOMAIN]["controller"].get_playlists(
            account, playlist_type, country_code, locale, limit
        )
        self._attributes["playlists"] = [{ "uri": x['uri'], "name": x['name']} for x in resp['items'] ]

        self._attributes["last_update"] = dt.now().isoformat("T")
        self._state = STATE_OK
