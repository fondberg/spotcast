"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.sensor.spotify_current_audio_features import (
    AbstractAudioFeatureSensor,
    STATE_UNKNOWN
)


class TestExistingFeature(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)

        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {
                "abstract": "bar"
            }
        }

        self.sensor = AbstractAudioFeatureSensor(self.account)

        await self.sensor.async_update()

    def test_state_was_updated(self):
        self.assertEqual(self.sensor._attr_state, "bar")


class TestMissingFeature(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.account = MagicMock(spec=SpotifyAccount)

        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {}
        }

        self.sensor = AbstractAudioFeatureSensor(self.account)

        await self.sensor.async_update()

    def test_state_was_updated(self):
        self.assertEqual(self.sensor._attr_state, STATE_UNKNOWN)
