from logging import getLogger
import logging
from time import sleep

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController
)
from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast
)

logging.basicConfig(level=logging.DEBUG)
LOGGER = getLogger(__name__)

print(LOGGER.level)

device = Chromecast.from_network(
    host="192.168.0.174",
    friendly_name="Bureau Felix"
)

LOGGER.debug("test")

device.wait()
device.set_volume(0.5)

account = SpotifyAccount(
    "felix",
    "AQDSErla3ENMsjBbg1YIFjnoOLP6M_HXQLKXxd7GO_VGi9YUkK0wMYQWAlohz3p0vASeU-Kupu5b1W4Oh61vw2ECkQd_Adbm9VRMZtigklKwWMybWx6IA7frbVELzS4tok4KJnrM-0iDbqiLYm5yKT9R5MT31liCy21p8hTQ4CGNMM6XpFi3E2V-MZ8Rp7HCNlMxduNuNTVuN6TDux_3nWjeddKm",
    "73078247-a5f0-463d-aaec-2ee490822b3f",
    "CA"
)
account.connect()

controller = SpotifyController(account)

device.register_handler(controller)
LOGGER.debug(device.status)
device.quit_app()
device.wait()

controller.launch_app(device, max_attempts=None)
