"""Module to test the async_get_config_entry_implementation function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from homeassistant.core import HomeAssistant

from custom_components.spotcast.sessions.public_session import (
    ConfigEntry,
    async_get_config_entry_implementation,
)

from test.sessions.public_session import TEST_MODULE


class TestImplementationExist(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_get_implementations")
    async def asyncSetUp(self, mock_implementations: AsyncMock):

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

    @patch(f"{TEST_MODULE}.async_get_implementations")
    async def test_correct_implementation_was_returned(
        self,
        mock_implementations: AsyncMock
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
