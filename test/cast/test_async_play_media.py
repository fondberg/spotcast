"""Module to test the async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.spotcast.cast import (
    async_play_media,
    HomeAssistant,
    Chromecast,
)

TEST_MODULE = "custom_components.spotcast.cast"


class TestValidMediaId(IsolatedAsyncioTestCase):

    @patch(
        f"{TEST_MODULE}.ha_spotify.spotify_uri_from_media_browser_url",
        new_callable=MagicMock
    )
    async def asyncSetUp(self, mock_uri: MagicMock):

        mock_uri.return_value = "spotify:artist:bar"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "cast": MagicMock(spec=Chromecast),
            "mock_uri": mock_uri,
        }

        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_call = AsyncMock()

        self.result = await async_play_media(
            self.mocks["hass"],
            "media_player.foo",
            self.mocks["cast"],
            media_type="spotify://artist",
            media_id="spotify://12345/spotify:artist:bar"
        )

    def test_returns_true(self):
        self.assertTrue(self.result)

    def test_proper_call_made(self):
        try:
            self.mocks["hass"].services.async_call.assert_called_with(
                "spotcast",
                "play_media",
                {
                    "media_player": {
                        "entity_id": [
                            "media_player.foo"
                        ]
                    },
                    "spotify_uri": "spotify:artist:bar"
                },
                blocking=False
            )
        except AssertionError:
            self.fail()


class TestInvalidMediaId(IsolatedAsyncioTestCase):

    @patch(
        f"{TEST_MODULE}.ha_spotify.spotify_uri_from_media_browser_url",
        new_callable=MagicMock
    )
    async def asyncSetUp(self, mock_uri: MagicMock):

        mock_uri.return_value = "spotify:artist:bar"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "cast": MagicMock(spec=Chromecast),
            "mock_uri": mock_uri,
        }

        self.mocks["hass"].services = MagicMock()
        self.mocks["hass"].services.async_call = AsyncMock()

        self.result = await async_play_media(
            self.mocks["hass"],
            "media_player.foo",
            self.mocks["cast"],
            media_type="spotify://artist",
            media_id=None
        )

    def test_returns_false(self):
        self.assertFalse(self.result)

    def test_no_service_call_made(self):
        try:
            self.mocks["hass"].services.async_call.assert_not_called()
        except AssertionError:
            self.fail()
