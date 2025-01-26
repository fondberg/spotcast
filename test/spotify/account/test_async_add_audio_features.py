"""Module to test the async_add_audio_features function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    PrivateSession,
    PublicSession,
    HomeAssistant,
    Spotify,
)


from test.spotify.account import TEST_MODULE


class TestNewItem(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": {}
        }

        self.account.async_track_features = AsyncMock()
        self.account.async_track_features.return_value = "baz"

        self.result = await self.account._async_add_audio_features({
            "item": {
                "uri": "spotify:track:bar"
            }
        })

    def test_expected_modification_to_playback(self):
        self.assertEqual(
            self.result,
            {
                "item": {
                    "uri": "spotify:track:bar"
                },
                "audio_features": "baz"
            }
        )


class TestSameItem(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": "far"
        }

        self.account.async_track_features = AsyncMock()
        self.account.async_track_features.return_value = "baz"

        self.result = await self.account._async_add_audio_features({
            "item": {
                "uri": "spotify:track:foo"
            }
        })

    def test_expected_modification_to_playback(self):
        self.assertEqual(
            self.result,
            {
                "item": {
                    "uri": "spotify:track:foo"
                },
                "audio_features": "far"
            }
        )


class TestNoCurrentPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify, new_callable=MagicMock)
    async def asyncSetUp(self, mock_spotify: MagicMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
            "spotify": mock_spotify.return_value,
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.account.current_item = {
            "uri": "spotify:track:foo",
            "audio_features": "far"
        }

        self.account.async_track_features = AsyncMock()
        self.account.async_track_features.return_value = "baz"

        self.result = await self.account._async_add_audio_features({
            "item": {}
        })

    def test_expected_modification_to_playback(self):
        self.assertEqual(
            self.result,
            {"item": {}}
        )


class TestNoneTypeState(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.result = await self.account._async_add_audio_features(None)

    def test_empty_dict_returned(self):
        self.assertEqual(self.result, {})


class TestItemKeyPointsToNoneType(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "public": MagicMock(spec=PublicSession),
            "private": MagicMock(spec=PrivateSession),
        }

        self.account = SpotifyAccount(
            entry_id="12345",
            hass=self.mocks["hass"],
            public_session=self.mocks["public"],
            private_session=self.mocks["private"],
        )

        self.result = await self.account._async_add_audio_features(
            {"items": None}
        )

    def test_empty_dict_returned(self):
        self.assertEqual(self.result, {"items": None})
