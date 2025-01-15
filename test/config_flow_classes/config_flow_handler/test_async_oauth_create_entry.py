"""Module to test the async_oauth_create_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import AbortFlow

from custom_components.spotcast.config_flow_classes.config_flow_handler \
    import (
        SpotcastFlowHandler,
        SOURCE_REAUTH,
        Spotify,
        PrivateSession,
        ConfigEntry,
    )

from test.config_flow_classes.config_flow_handler import TEST_MODULE


class TestExternalApiEntry(IsolatedAsyncioTestCase):

    def setUp(self):

        self.external_api = {
            "auth_implementation": "spotcast_foo",
            "token": {
                "access_token": "12345",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refreh_token": "ABCDF",
                "expires_at": 1729807129.8667192
            }
        }

        self.flow_handler = SpotcastFlowHandler()

    @patch.object(
        SpotcastFlowHandler,
        "async_show_form",
        new_callable=MagicMock
    )
    async def test_data_attributes_has_external_api_data(
        self,
        mock_form: MagicMock
    ):
        await self.flow_handler.async_oauth_create_entry(self.external_api)
        self.assertIn("external_api", self.flow_handler.data)

    @patch.object(
        SpotcastFlowHandler,
        "async_show_form",
        new_callable=MagicMock
    )
    async def test_intern_api_step_is_called(self, mock_form: MagicMock):
        await self.flow_handler.async_oauth_create_entry(self.external_api)
        try:
            mock_form.assert_called_with(
                step_id="internal_api",
                data_schema=self.flow_handler.INTERNAL_API_SCHEMA,
                errors={},
            )
        except AssertionError:
            self.fail("internal_api step was never called")


class TestInternalApiProvided(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
        }

        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(return_value={
            "id": "foo",
            "display_name": "User Name"
        })

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.async_set_unique_id = AsyncMock()
        self.handler.async_create_entry = MagicMock()
        self.mocks["hass"].config_entries.async_entries.return_value = []

        self.result = await self.handler.async_oauth_create_entry({})

    def test_entry_properly_setup(self):
        try:
            self.handler.async_create_entry(
                title="User Name",
                data={
                    "external_api": {
                        "token": {
                            "access_token": "12345"
                        }
                    },
                    "internal_api": {
                        "sp_dc": "foo",
                        "sp_key": "bar"
                    }
                },
                options={
                    "is_default": True,
                    "base_refresh_rate": 30,
                }
            )
        except AssertionError:
            self.fail()


class TestImportingFromYAMLConfig(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
        }

        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(return_value={
            "id": "foo",
            "display_name": "User Name"
        })

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler._import_data = {"sp_dc": "foo", "sp_key": "bar"}
        self.handler.async_set_unique_id = AsyncMock()
        self.handler.async_create_entry = MagicMock()
        self.mocks["hass"].config_entries.async_entries.return_value = []

        self.result = await self.handler.async_oauth_create_entry({})

    def test_entry_properly_setup(self):
        try:
            self.handler.async_create_entry(
                title="User Name",
                data={
                    "external_api": {
                        "token": {
                            "access_token": "12345"
                        }
                    },
                    "internal_api": {
                        "sp_dc": "foo",
                        "sp_key": "bar"
                    }
                },
                options={
                    "is_default": True,
                    "base_refresh_rate": 30,
                }
            )
        except AssertionError:
            self.fail()


class TestFailedToGetProfile(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
        }

        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(
            side_effect=ValueError()
        )

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.async_abort = MagicMock()

        self.result = await self.handler.async_oauth_create_entry({})

    def test_abort_correctly_called(self):
        try:
            self.handler.async_abort(reason="connection_error")
        except AssertionError:
            self.fail()


class TestPublicPrivateProfileMismatch(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
        }

        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(side_effect=[
            {
                "id": "foo",
                "display_name": "User Name"
            },
            {
                "id": "bar",
                "display_name": "Different User"
            }
        ])

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.async_abort = MagicMock()

        self.result = await self.handler.async_oauth_create_entry({})

    def test_abort_correctly_called(self):
        try:
            self.handler.async_abort.assert_called_with(
                reason="public_private_accounts_mismatch"
            )
        except AssertionError:
            self.fail()


class TestReauthProcess(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def asyncSetUp(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].unique_id = "foo"
        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(side_effect=[
            {
                "id": "foo",
            },
            {
                "id": "foo",
            }
        ])

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.context = {
            "source": SOURCE_REAUTH,
            "unique_id": "foo"
        }
        self.handler._get_reauth_entry = MagicMock(
            return_value=self.mocks["entry"]
        )
        self.handler.async_update_reload_and_abort = MagicMock()

        self.result = await self.handler.async_oauth_create_entry({})

    def test_abort_correctly_called(self):
        try:
            self.handler.async_update_reload_and_abort.assert_called_with(
                self.mocks["entry"],
                title="foo",
                data=self.handler.data,
            )
        except AssertionError:
            self.fail()


class TestFailReauthProcess(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def test_error_raised(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].unique_id = "bar"
        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(side_effect=[
            {
                "id": "foo",
            },
            {
                "id": "foo",
            }
        ])

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.context = {
            "source": SOURCE_REAUTH,
            "unique_id": "bar"
        }
        self.handler._get_reauth_entry = MagicMock(
            return_value=self.mocks["entry"]
        )
        self.handler.async_update_reload_and_abort = MagicMock()

        with self.assertRaises(AbortFlow):
            await self.handler.async_oauth_create_entry({})


class TestUniqueIdExist(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.Spotify", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.PrivateSession", new_callable=MagicMock)
    async def test_error_raised(
        self,
        mock_private: MagicMock,
        mock_spotify: MagicMock,
    ):

        mock_private.return_value = MagicMock(spec=PrivateSession)
        mock_spotify.return_value = MagicMock(spec=Spotify)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "private": mock_private.return_value,
            "spotify": mock_spotify.return_value,
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].unique_id = "bar"
        self.mocks["private"].token = "23456"
        self.mocks["hass"].async_add_executor_job = AsyncMock(side_effect=[
            {
                "id": "foo",
            },
            {
                "id": "foo",
            }
        ])

        self.data = {
            "external_api": {
                "token": {
                    "access_token": "12345"
                }
            },
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.handler = SpotcastFlowHandler()
        self.handler.hass = self.mocks["hass"]
        self.handler.data = self.data
        self.handler.context = {
            "source": SOURCE_REAUTH,
            "unique_id": "bar"
        }
        self.handler._get_reauth_entry = MagicMock(
            return_value=self.mocks["entry"]
        )
        self.handler.async_update_reload_and_abort = MagicMock()
        self.handler._abort_if_unique_id_configured = MagicMock(
            side_effect=AbortFlow(reason="test_abort")
        )

        with self.assertRaises(AbortFlow):
            await self.handler.async_oauth_create_entry({})
