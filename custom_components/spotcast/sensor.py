import logging
import json
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt
from homeassistant.const import STATE_OK, STATE_UNKNOWN
import homeassistant.components.zeroconf as zc
import pychromecast
from . import DOMAIN
from homeassistant.components.cast.helpers import ChromeCastZeroconf
_LOGGER = logging.getLogger(__name__)
SENSOR_SCAN_INTERVAL_SECS = 30
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
        known_devices, browser = pychromecast.get_chromecasts(zeroconf_instance=ChromeCastZeroconf.get_zeroconf())
        browser.stop_discovery()
        _LOGGER.debug('devices %s', known_devices)
        chromecasts = [
            {
                "host": str(k.socket_client.host),
                "port": k.socket_client.port,
                "uuid": str(k.uuid),
                "model_name": k.model_name,
                "name": k.name,
                'manufacturer': k.device.manufacturer
            }
            for k in known_devices
        ]

        self._attributes['devices_json'] = json.dumps(chromecasts, ensure_ascii=False)
        self._attributes['devices'] = chromecasts
        self._attributes['last_update'] = dt.now().isoformat('T')
        self._state = STATE_OK
