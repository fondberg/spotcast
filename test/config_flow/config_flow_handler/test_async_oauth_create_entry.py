"""Module to test the async_oauth_create_entry function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock

from spotipy import Spotify

from custom_components.spotcast.config_flow.config_flow_handler import (
    SpotcastFlowHandler
)

from test.unit_utils import AsyncMock

TEST_MODULE = "custom_components.spotcast.config_flow.config_flow_handler"


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

    @patch.object(SpotcastFlowHandler, "async_show_form")
    async def test_data_attributes_has_external_api_data(
        self,
        mock_form: MagicMock
    ):
        await self.flow_handler.async_oauth_create_entry(self.external_api)
        self.assertIn("external_api", self.flow_handler.data)

    @patch.object(SpotcastFlowHandler, "async_show_form")
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


class TestInternalApiEntry(IsolatedAsyncioTestCase):

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

        self.internal_api = {
            "sp_dc": "foo",
            "sp_key": "bar",
        }

        self.flow_handler = SpotcastFlowHandler()
        self.flow_handler.data = {
            "external_api": self.external_api,
            "internal_api": self.internal_api,
        }

    @patch.object(SpotcastFlowHandler, "async_set_unique_id", new_callable=AsyncMock)
    @patch.object(SpotcastFlowHandler, "hass", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def test_spotify_object_created_with_proper_access_token(
            self,
            mock_spotify: MagicMock,
            mock_hass: MagicMock,
            mock_set_id: MagicMock,
    ):

        mock_hass.async_add_executor_job.return_value = {
            "id": "foo",
            "display_name": "Dummy User",
        }

        mock_hass.config_entries.async_entries = MagicMock(
            return_value=[
                "foo"
            ]
        )

        await self.flow_handler.async_oauth_create_entry(
            self.flow_handler.data
        )

        try:
            mock_spotify.assert_called_with("12345")
        except AssertionError:
            self.fail("Spotify constructor called with wrong token")

    @patch.object(SpotcastFlowHandler, "async_create_entry")
    @patch.object(SpotcastFlowHandler, "async_set_unique_id", new_callable=AsyncMock)
    @patch.object(SpotcastFlowHandler, "hass", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def test_entry_setup_with_expected_data(
            self,
            mock_spotify: MagicMock,
            mock_hass: MagicMock,
            mock_set_id: MagicMock,
            mock_entry: MagicMock,
    ):

        mock_hass.async_add_executor_job.return_value = {
            "id": "foo",
            "display_name": "Dummy User",
        }

        mock_hass.config_entries.async_entries = MagicMock(
            return_value=[
                "foo"
            ]
        )

        await self.flow_handler.async_oauth_create_entry(
            self.flow_handler.data
        )

        try:
            mock_entry.assert_called_with(
                title="Dummy User",
                data={
                    "name": "Dummy User",
                    "external_api": self.external_api,
                    "internal_api": self.internal_api,
                    "is_default": False,
                }
            )
        except AssertionError:
            self.fail("Wrong arguments provided to entry creation")

    @patch.object(SpotcastFlowHandler, "async_create_entry")
    @patch.object(SpotcastFlowHandler, "async_set_unique_id", new_callable=AsyncMock)
    @patch.object(SpotcastFlowHandler, "hass", new_callable=AsyncMock)
    @patch(f"{TEST_MODULE}.Spotify", spec=Spotify)
    async def test_name_is_id_when_missing_display_name(
            self,
            mock_spotify: MagicMock,
            mock_hass: MagicMock,
            mock_set_id: MagicMock,
            mock_entry: MagicMock,
    ):

        mock_hass.async_add_executor_job.return_value = {
            "id": "foo",
        }

        mock_hass.config_entries.async_entries = MagicMock(return_value=[])

        await self.flow_handler.async_oauth_create_entry(
            self.flow_handler.data
        )

        try:
            mock_entry.assert_called_with(
                title="foo",
                data={
                    "name": "foo",
                    "external_api": self.external_api,
                    "internal_api": self.internal_api,
                    "is_default": True,
                }
            )
        except AssertionError:
            self.fail("Wrong arguments provided to entry creation")


class TestCurrentUserFail(IsolatedAsyncioTestCase):

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

        self.internal_api = {
            "sp_dc": "foo",
            "sp_key": "bar",
        }

        self.flow_handler = SpotcastFlowHandler()
        self.flow_handler.data = {
            "external_api": self.external_api,
            "internal_api": self.internal_api,
        }

    @patch.object(SpotcastFlowHandler, "async_abort")
    async def test_abort_sent(self, mock_abort: MagicMock):

        await self.flow_handler.async_oauth_create_entry(
            self.flow_handler.data
        )

        try:
            mock_abort.assert_called_once()
        except AssertionError:
            self.fail("Abort was not called")
