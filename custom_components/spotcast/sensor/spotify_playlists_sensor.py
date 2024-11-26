"""The SpotifyPlaylistsSensor object

Classes:
    - SpotifyPlaylistsSensor
"""

from logging import getLogger
from urllib3.exceptions import ReadTimeoutError

from homeassistant.const import STATE_UNKNOWN
from requests.exceptions import ReadTimeout

from custom_components.spotcast.sensor.abstract_sensor import SpotcastSensor
from custom_components.spotcast.utils import copy_to_dict

LOGGER = getLogger(__name__)


class SpotifyPlaylistsSensor(SpotcastSensor):
    """A Home Assistant sensor reporting available playlists for a
    Spotify Account

    Properties:
        - state_class(str): the state class of the entity

    Methods:
        - async_update
    """

    GENERIC_NAME = "Spotify Playlists"
    ICON = "mdi:playlist-music"
    ICON_OFF = ICON
    DEFAULT_ATTRIBUTES = {"first_10_playlists": []}
    UNITS_OF_MEASURE = "playlists"

    async def async_update(self):
        """Updates the playlist count asynchornously"""

        try:
            count = await self.account.async_playlists_count()
            playlists = await self.account.async_playlists(max_items=10)
        except (ReadTimeoutError, ReadTimeout):
            self._attr_state = STATE_UNKNOWN
            self._attributes["first_10_playlists"] = []
            return

        LOGGER.debug(
            "Found %d playlist for spotify account `%s`",
            count,
            self.account.name
        )

        self._attr_state = count
        top_10 = [self._clean_playlist(x) for x in playlists]
        self._attributes["first_10_playlists"] = top_10

    @staticmethod
    def _clean_playlist(playlist: dict) -> dict:
        """Cleans a playlist for attributes in Home Assistant"""
        keep = (
            "description",
            "name",
            "owner",
            "collaborative",
            "uri",
            "image",
        )

        playlist = copy_to_dict(playlist)

        playlist["owner"] = playlist["owner"]["id"]

        max_area = -1

        for image in playlist["images"]:

            try:
                area = image["height"] * image["width"]
            except TypeError:
                area = 0

            if area > max_area:
                playlist["image"] = image["url"]
                max_area = area

        result = {}

        for key, value in playlist.items():
            if key in keep:
                result[key] = value

        return result
