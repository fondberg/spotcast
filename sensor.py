import logging
import json
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt
from homeassistant.const import (STATE_OK, STATE_UNKNOWN)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([ChromecastDevicesSensor()])


class ChromecastDevicesSensor(Entity):

    def __init__(self):
        self._state = STATE_UNKNOWN
        self._chromecast_devices = []
        self._attributes = {
            'devices_json': [],
            'last_update': None
        }
        self.update()

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
        import pychromecast
        _LOGGER.debug('updating')
        self._chromecast_devices = pychromecast.get_chromecasts()
        _LOGGER.debug('Found chromecast devices: %s', self._chromecast_devices)
        # self._attributes['devices'] = [cast.name for cast in self._chromecast_devices]
        chromecasts = []
        for cast in self._chromecast_devices:
            device = {
                'name': cast.name,
                'cast_type': cast.cast_type,
                'model_name': cast.model_name,
                'uuid': str(cast.uuid),
                'manufacturer': cast.device.manufacturer
            }
            chromecasts.append(device)
        self._attributes['devices_json'] = json.dumps(chromecasts, ensure_ascii=False)
        self._attributes['last_update'] = dt.now().isoformat('T')
        self._state = STATE_OK


