"""Module to test the async_play_dj function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_dj import (
    async_play_dj,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_dj"


class TestBaseMediaPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
        self,
        mock_play_media: AsyncMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play_media": mock_play_media,
        }

        self.mocks["call"].data = {
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "volume": 80,
                "shuffle": True,
            }
        }

        await async_play_dj(self.mocks["hass"], self.mocks["call"])

    def test_async_play_media_was_called(self):
        try:
            self.mocks["play_media"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_values_after_call(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "account": "12345",
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "data": {
                    "volume": 80,
                },
                "spotify_uri": SpotifyAccount.DJ_URI
            }
        )


class TestMediaPlaybackWithoutExtras(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_play_media")
    async def asyncSetUp(
        self,
        mock_play_media: AsyncMock,
    ):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "play_media": mock_play_media,
        }

        self.mocks["call"].data = {
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": None
        }

        await async_play_dj(self.mocks["hass"], self.mocks["call"])

    def test_async_play_media_was_called(self):
        try:
            self.mocks["play_media"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_values_after_call(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "account": "12345",
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "data": None,
                "spotify_uri": SpotifyAccount.DJ_URI
            }
        )
