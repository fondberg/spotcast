"""Module to test async_play_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_media import (
    async_play_media,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
    ServiceValidationError,
    MissingActiveDeviceError,
)

TEST_MODULE = "custom_components.spotcast.services.play_media"


class TestBaseMediaPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "volume": 80
            }
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].async_play_media\
                .assert_called_with("12345", "dummy_uri", volume=80)
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()


class TestEmptyExtras(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].return_value.async_play_media\
                .assert_called_with("12345", "dummy_uri")
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].return_value.async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()


class TestTransferPlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": None,
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].return_value.async_play_media\
                .assert_called_with("12345", None)
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].return_value.async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()


class TestTrackUri(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_track_index")
    @patch(f"{TEST_MODULE}.async_random_index")
    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
        mock_random: AsyncMock,
        mock_index: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
            "random": mock_random,
            "index": mock_index,
        }

        self.mocks["index"].return_value = ("spotify:album:foo", 5)
        self.mocks["call"].data = {
            "spotify_uri": "spotify:track:bar",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "random": True,
            }
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].async_play_media\
                .assert_called_with(
                    "12345",
                    "spotify:album:foo",
                    random=True,
                    offset=4,
            )
        except AssertionError:
            self.fail()

    def test_random_offset_ignored_in_case_of_track_uri(self):
        try:
            self.mocks["random"].assert_not_called()
        except AssertionError:
            self.fail()


class TestRandomOffsetRequested(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_random_index")
    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
            self,
            mock_entry: MagicMock,
            mock_account: AsyncMock,
            mock_player: AsyncMock,
            mock_random: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
            "random": mock_random,
        }

        self.mocks["random"].return_value = 5

        self.mocks["call"].data = {
            "spotify_uri": "spotify:album:bar",
            "account": "12345",
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            },
            "data": {
                "random": True,
            }
        }

        self.result = await async_play_media(
            self.mocks["hass"],
            self.mocks["call"],
        )

    def test_random_index_requested(self):
        try:
            self.mocks["account"].async_play_media.assert_called_with(
                "12345",
                "spotify:album:bar",
                random=True,
                offset=5
            )
        except AssertionError:
            self.fail()


class TestActiveDevicePlayback(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.return_value.id = "12345"

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "data": {
                "volume": 80
            }
        }

        await async_play_media(self.mocks["hass"], self.mocks["call"])

    def test_account_play_media_called_with_expected_arguments(self):
        try:
            self.mocks["account"].async_play_media\
                .assert_called_with("12345", "dummy_uri", volume=80)
        except AssertionError:
            self.fail()

    def test_account_apply_extra_called(self):
        try:
            self.mocks["account"].async_apply_extras\
                .assert_called()
        except AssertionError:
            self.fail()


class TestMissingActiveDevice(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_media_player_from_id")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def test_error_raised(
        self,
        mock_entry: MagicMock,
        mock_account: AsyncMock,
        mock_player: AsyncMock,
    ):

        mock_entry.return_value = MagicMock()
        mock_account.return_value = MagicMock(spec=SpotifyAccount)
        mock_player.side_effect = MissingActiveDeviceError()

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "entry": mock_entry(),
            "account": mock_account.return_value,
            "player": mock_player(),
        }

        self.mocks["call"].data = {
            "spotify_uri": "dummy_uri",
            "account": "12345",
            "data": {
                "volume": 80
            }
        }

        with self.assertRaises(ServiceValidationError):
            await async_play_media(self.mocks["hass"], self.mocks["call"])
