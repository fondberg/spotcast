"""Module to test the device_class property"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    CurrentTrackValenceSensor,
)


class TestMissingValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {}
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-outline")


class TestVeryHighValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "valence": 0.99
            }
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-excited")


class TestHighValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "valence": 0.75
            }
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-happy")


class TestNeutralValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "valence": 0.5
            }
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-neutral")


class TestLowValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "valence": 0.3
            }
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-sad")


class TestVeryLowValence(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "valence": 0.05
            }
        }
        self.sensor = CurrentTrackValenceSensor(self.account)
        await self.sensor.async_update()

    def test_sensor_defined_as_sound_pressure_device(self):
        self.assertEqual(self.sensor.icon, "mdi:emoticon-cry")
