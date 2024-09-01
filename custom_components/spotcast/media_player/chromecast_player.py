"""Module containing the chromecast media player implementation"""

from pychromecast import Chromecast as ParentChromecast

from homeassistant.components.cast.media_player import CastDevice

from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer,
)


class Chromecast(ParentChromecast, MediaPlayer):

    PLATFORM = "cast"
    DEVICE_TYPE = CastDevice
