"""Module to test the async_get_config_entry_implementation function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.oauth2_session import (
    ConfigEntry,
    async_get_config_entry_implementation,
)

from test.unit_utils import AsyncMock


class TestImplementationExist(IsolatedAsyncioTestCase):

    @patch(
        "custom_components.spotcast.sessions.oauth2_session."
        "async_get_implementations",
        new_callable=AsyncMock
    )
    async def asyncSetUp(self, mock_implementations: MagicMock):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "external_api": {
                "auth_implementation": "foo"
            }
        }

        mock_entry.domain = "spotcast"

        mock_implementations.return_value = {
            "foo": "dummy_implementation"
        }

        self.result = await async_get_config_entry_implementation(
            mock_hass,
            mock_entry
        )

    async def test_correct_implementation_was_returned(self):
        self.assertEqual(self.result, "dummy_implementation")


class TestImplementationDoesntExist(IsolatedAsyncioTestCase):

    @patch(
        "custom_components.spotcast.sessions.oauth2_session."
        "async_get_implementations",
        new_callable=AsyncMock
    )
    async def test_correct_implementation_was_returned(
        self,
        mock_implementations: MagicMock
    ):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_entry = MagicMock(spec=ConfigEntry)

        mock_entry.data = {
            "external_api": {
                "auth_implementation": "foo"
            }
        }

        mock_entry.domain = "spotcast"

        mock_implementations.return_value = {
            "bar": "dummy_implementation"
        }

        with self.assertRaises(ValueError):
            await async_get_config_entry_implementation(
                mock_hass,
                mock_entry
            )
