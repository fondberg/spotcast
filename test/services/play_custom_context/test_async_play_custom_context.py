"""Module to test the async_play_custom_context function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_custom_context import (
    async_play_custom_context,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
    MissingActiveDeviceError,
    ServiceValidationError,
)
from custom_components.spotcast.media_player._abstract_player import (
    MediaPlayer
)

TEST_MODULE = "custom_components.spotcast.services.play_custom_context"


class TestPlayContext(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_media_player: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_media_player.return_value = MagicMock(spec=MediaPlayer)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "media_player": mock_media_player.return_value,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "tracks": ["foo", "bar"]
        }

        self.mocks["hass"].data = {}
        self.mocks["media_player"].id = "12345"

        await async_play_custom_context(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_async_play_media_called_properly(self):
        try:
            self.mocks["account"].async_play_media.assert_called_with(
                "12345",
                uris=["foo", "bar"],
            )
        except AssertionError:
            self.fail()

    def test_apply_extras_called_properly(self):
        try:
            self.mocks["account"].async_apply_extras(
                "12345",
                None
            )
        except AssertionError:
            self.fail()


class TestPlayContextWithExtras(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.randint", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_media_player: AsyncMock,
            mock_random: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_media_player.return_value = MagicMock(spec=MediaPlayer)
        mock_random.return_value = 1

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "media_player": mock_media_player.return_value,
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "tracks": ["foo", "bar"],
            "data": {
                "volume": 80,
                "position_ms": 5000,
                "random": True,
            }
        }

        self.mocks["hass"].data = {}
        self.mocks["media_player"].id = "12345"

        await async_play_custom_context(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_async_play_media_called_properly(self):
        try:
            self.mocks["account"].async_play_media.assert_called_with(
                "12345",
                uris=["foo", "bar"],
                position_ms=5000,
                volume=80,
                random=True,
                offset=1,
            )
        except AssertionError:
            self.fail()

    def test_apply_extras_called_properly(self):
        try:
            self.mocks["account"].async_apply_extras(
                "12345",
                {
                    "volume": 80,
                    "position_ms": 5000,
                    "random": True,
                    "offset": 1,
                }
            )
        except AssertionError:
            self.fail()


class TestPlayContextFromActiveDevice(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_media_player: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_media_player.return_value = MagicMock(spec=MediaPlayer)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "media_player": mock_media_player.return_value,
        }

        self.mocks["call"].data = {
            "tracks": ["foo", "bar"]
        }

        self.mocks["hass"].data = {}
        self.mocks["media_player"].id = "12345"

        await async_play_custom_context(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_async_play_media_called_properly(self):
        try:
            self.mocks["account"].async_play_media.assert_called_with(
                "12345",
                uris=["foo", "bar"],
            )
        except AssertionError:
            self.fail()

    def test_apply_extras_called_properly(self):
        try:
            self.mocks["account"].async_apply_extras(
                "12345",
                None
            )
        except AssertionError:
            self.fail()


class TestMissingActiveDevice(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def test_error_raised(
            self,
            mock_account: AsyncMock,
            mock_entry: MagicMock,
            mock_media_player: AsyncMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_media_player.side_effect = MissingActiveDeviceError()

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "media_player": mock_media_player.return_value,
        }

        self.mocks["call"].data = {
            "tracks": ["foo", "bar"]
        }

        self.mocks["hass"].data = {}
        self.mocks["media_player"].id = "12345"

        with self.assertRaises(ServiceValidationError):
            await async_play_custom_context(
                self.mocks["hass"],
                self.mocks["call"],
            )
