"""Module to test the system_health_info function"""

import inspect

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.system_health import (
    system_health_info,
    HomeAssistant,
    __version__,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.system_health"


class TestHealthyAccount(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_check_can_reach_url")
    async def asyncSetUp(self, mock_url_check: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": MagicMock(spec=SpotifyAccount),
            "url_check": mock_url_check,
        }

        self.mocks["hass"].data = {
            "spotcast": {
                "1234": {
                    "account": self.mocks["account"]
                }
            }
        }

        self.mocks["account"].health_status = {
            "external": True,
            "internal": True,
        }

        self.mocks["account"].id = "dummy"
        self.mocks["account"].is_default = True

        self.result = await system_health_info(self.mocks["hass"])

    def test_results_contain_current_version(self):
        self.assertIn("Version", self.result)
        self.assertEqual(self.result["Version"], __version__)

    def test_results_set_user_as_default(self):
        self.assertIn("Dummy Is Default", self.result)
        self.assertTrue(self.result["Dummy Is Default"])

    def test_url_tests_are_coroutines(self):
        self.assertIn("Dummy Public Endpoint", self.result)
        self.assertTrue(
            inspect.iscoroutine(self.result["Dummy Public Endpoint"])
        )


class TestUnHealthyAccount(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.async_check_can_reach_url")
    async def asyncSetUp(self, mock_url_check: AsyncMock):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account": MagicMock(spec=SpotifyAccount),
            "url_check": mock_url_check,
        }

        self.mocks["hass"].data = {
            "spotcast": {
                "1234": {
                    "account": self.mocks["account"]
                }
            }
        }

        self.mocks["account"].health_status = {
            "external": False,
            "internal": False,
        }

        self.mocks["account"].id = "dummy"
        self.mocks["account"].is_default = True

        self.result = await system_health_info(self.mocks["hass"])

    def test_proper_failed_check_object(self):
        self.assertEqual(
            self.result["Dummy Public Token"],
            {"type": "failed", "error": "unhealthy"},
        )
