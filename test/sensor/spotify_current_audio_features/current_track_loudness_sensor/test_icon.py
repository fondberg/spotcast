"""Module to test the device_class property"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackLoudnessSensor,
)


class TestMissingLoudness(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {}
        }
        self.sensor = CurrentTrackLoudnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:volume-off")


class TestLowVolumeSong(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "loudness": -50
            }
        }
        self.sensor = CurrentTrackLoudnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:volume-low")


class TestMediumVolumeSong(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "loudness": -30.0
            }
        }
        self.sensor = CurrentTrackLoudnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:volume-medium")


class TestHighVolumeSong(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "loudness": -10
            }
        }
        self.sensor = CurrentTrackLoudnessSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:volume-high")
