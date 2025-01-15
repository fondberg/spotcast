"""Module to test the build_from_integration function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.media_player.utils import (
    async_build_from_type,
    CastDevice,
    Chromecast,
    SpotifyDevice,
    UnknownIntegrationError,
    HomeAssistant,
    SpotifyAccount,
    SpotifyController,
)

TEST_MODULE = "custom_components.spotcast.media_player.utils"


class DummyDevice:

    def __init__(self):
        pass


class TestCastDeviceNotRunningAnApp(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_cast_info = MagicMock()
        self.mock_cast_info.cast_type = "foo"

        self.mock_hass.async_add_executor_job = AsyncMock()

        self.mock_entity = MagicMock(spec=CastDevice)
        self.mock_entity._cast_info = MagicMock()
        self.mock_entity._cast_info.cast_info = self.mock_cast_info
        self.mock_entity.app_id = None
        self.mock_entity.quit_app = MagicMock()

        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)

    def test_quit_app_not_run(self):
        try:
            self.mock_entity.quit_app.assert_not_called()
        except AssertionError:
            self.fail()


class TestCastDeviceRunningSpotifyForCurrentUser(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Chromecast")
    async def asyncSetUp(self, mock_player: MagicMock):

        mock_player.return_value = MagicMock(spec=Chromecast)

        self.mocks = {
            "account": MagicMock(spec=SpotifyAccount),
            "hass": MagicMock(spec=HomeAssistant),
            "cast_info": MagicMock(),
            "entity": MagicMock(spec=CastDevice),
            "media_player": mock_player.return_value,
        }

        self.mocks["account"] = MagicMock(spec=SpotifyAccount)
        self.mocks["hass"] = MagicMock(spec=HomeAssistant)
        self.mocks["cast_info"] = MagicMock()
        self.mocks["cast_info"].cast_type = "foo"

        self.mocks["hass"].async_add_executor_job = AsyncMock()

        self.mocks["entity"] = MagicMock(spec=CastDevice)
        self.mocks["entity"]._cast_info = MagicMock()
        self.mocks["entity"]._cast_info.cast_info = self.mocks["cast_info"]
        self.mocks["media_player"].app_id = SpotifyController.APP_ID
        self.mocks["entity"].quit_app = MagicMock()
        self.mocks["account"].active_device = "12345"
        self.mocks["media_player"].id = "12345"
        self.mocks["media_player"].register_handler = MagicMock()

        self.result = await async_build_from_type(
            hass=self.mocks["hass"],
            entity=self.mocks["entity"],
            account=self.mocks["account"],
        )

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)

    def test_quit_app_not_run(self):
        try:
            self.mocks["entity"].quit_app.assert_not_called()
        except AssertionError:
            self.fail()

    def test_launch_app_not_run(self):
        self.assertEqual(
            self.mocks["hass"].async_add_executor_job.call_count,
            1,
        )


class TestCastDeviceRunningNonSpotifyApp(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Chromecast", new_callable=MagicMock)
    async def asyncSetUp(self, mock_chromecast: MagicMock):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_cast_info = MagicMock()
        self.mock_cast_info.cast_type = "foo"

        self.mock_hass.async_add_executor_job = AsyncMock()

        self.mock_entity = MagicMock(spec=CastDevice)
        self.mock_entity._cast_info = MagicMock()
        self.mock_entity._cast_info.cast_info = self.mock_cast_info
        self.mock_entity.app_id = "CC123523462345"
        self.mock_entity.quit_app = MagicMock()
        self.mock_account.active_device = "12345"
        self.mock_entity.id = "12345"

        mock_chromecast.return_value = MagicMock(spec=Chromecast)
        self.mock_chromecast = mock_chromecast.return_value
        self.mock_chromecast.app_id = self.mock_entity.app_id
        self.mock_chromecast.id = "12345"
        self.mock_chromecast.wait = MagicMock()
        self.mock_chromecast.quit_app = MagicMock()
        self.mock_chromecast.register_handler = MagicMock()

        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)

    def test_quit_app_not_run(self):
        try:
            self.mock_chromecast.quit_app.assert_called()
        except AssertionError:
            self.fail()


class TestCastDeviceRunningSpotifyAppForOtherAccount(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Chromecast", new_callable=MagicMock)
    async def asyncSetUp(self, mock_chromecast: MagicMock):

        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_cast_info = MagicMock()
        self.mock_cast_info.cast_type = "foo"

        self.mock_hass.async_add_executor_job = AsyncMock()

        self.mock_entity = MagicMock(spec=CastDevice)
        self.mock_entity._cast_info = MagicMock()
        self.mock_entity._cast_info.cast_info = self.mock_cast_info
        self.mock_entity.app_id = SpotifyController.APP_ID
        self.mock_entity.quit_app = MagicMock()
        self.mock_account.active_device = "23456"
        self.mock_entity.id = "12345"

        mock_chromecast.return_value = MagicMock(spec=Chromecast)
        self.mock_chromecast = mock_chromecast.return_value
        self.mock_chromecast.app_id = self.mock_entity.app_id
        self.mock_chromecast.id = "12345"
        self.mock_chromecast.wait = MagicMock()
        self.mock_chromecast.quit_app = MagicMock()
        self.mock_chromecast.register_handler = MagicMock()

        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIsInstance(self.result, Chromecast)

    def test_quit_app_not_run(self):
        try:
            self.mock_chromecast.quit_app.assert_called()
        except AssertionError:
            self.fail()


class TestSpotifyDeviceCreation(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_account = MagicMock(spec=SpotifyAccount)
        self.mock_entity = MagicMock(spec=SpotifyDevice)
        self.result = await async_build_from_type(
            self.mock_hass,
            self.mock_entity,
            self.mock_account,
        )

    def test_chromecast_device_returned(self):
        self.assertIs(self.result, self.mock_entity)


class TestNoneManagedDeviceCreation(IsolatedAsyncioTestCase):

    async def test_error_raised(self):
        self.mock_entity = DummyDevice()
        self.mock_hass = MagicMock(spec=HomeAssistant)
        self.mock_account = MagicMock(spec=SpotifyDevice)

        with self.assertRaises(UnknownIntegrationError):
            await async_build_from_type(
                self.mock_hass,
                self.mock_entity,
                self.mock_account,
            )
