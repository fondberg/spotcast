"""Module to test the icon property"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackAcousticnessSensor,
)


class TestMissingAcousticness(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {}
        }
        self.sensor = CurrentTrackAcousticnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:guitar-acoustic")


class TestLowAcusticness(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "acousticness": 0.25
            }
        }
        self.sensor = CurrentTrackAcousticnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:guitar-electric")


class TestHighAcousticness(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "acousticness": 0.75
            }
        }
        self.sensor = CurrentTrackAcousticnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:guitar-acoustic")
