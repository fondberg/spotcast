import logging
import json
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt
from homeassistant.const import STATE_OK, STATE_UNKNOWN

from . import DOMAIN, KNOWN_CHROMECAST_INFO_KEY

_LOGGER = logging.getLogger(__name__)

SENSOR_SCAN_INTERVAL_SECS = 10
SCAN_INTERVAL = timedelta(seconds=SENSOR_SCAN_INTERVAL_SECS)


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([ChromecastDevicesSensor(hass)])

class ChromecastDevicesSensor(Entity):

    def __init__(self, hass):
        self.hass = hass
        self._state = STATE_UNKNOWN
        self._chromecast_devices = []
        self._attributes = {
            'devices_json': [],
            'devices': [],
            'last_update': None
        }
        _LOGGER.debug('initiating sensor')

    @property
    def name(self):
        return 'Chromecast Devices'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        _LOGGER.debug('Getting chromecast devices')

        known_devices = self.hass.data.get(KNOWN_CHROMECAST_INFO_KEY, [])

        _LOGGER.debug('devices %s', known_devices)

        chromecasts = [
            {
                "host": str(known_devices[k].host),
                "port": known_devices[k].port,
                "uuid": known_devices[k].uuid,
                "model_name": known_devices[k].model_name,
                "name": known_devices[k].friendly_name,
                'manufacturer': known_devices[k].manufacturer
            }
            for k in known_devices
        ]

        self._attributes['devices_json'] = json.dumps(chromecasts, ensure_ascii=False)
        self._attributes['devices'] = chromecasts
        self._attributes['last_update'] = dt.now().isoformat('T')
        self._state = STATE_OK



