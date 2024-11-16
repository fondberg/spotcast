"""Module to test the async_get_accounts function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from custom_components.spotcast.websocket.accounts_handler import (
    async_get_accounts,
    HomeAssistant,
    ActiveConnection,
    SpotifyAccount,
)


class TestAccountRetrieval(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "account_a": MagicMock(spec=SpotifyAccount),
            "account_b": MagicMock(spec=SpotifyAccount),
            "connection": MagicMock(spec=ActiveConnection),
        }

        self.mocks["account_a"].id = "id_a"
        self.mocks["account_a"].name = "Name A"
        self.mocks["account_a"].is_default = True
        self.mocks["account_a"].country = "CA"
        self.mocks["account_b"].id = "id_b"
        self.mocks["account_b"].name = "Name B"
        self.mocks["account_b"].is_default = False
        self.mocks["account_b"].country = "CA"

        self.mocks["hass"].data = {
            "spotcast": {
                "12345": {
                    "account": self.mocks["account_a"],
                },
                "23456": {
                    "account": self.mocks["account_b"],
                },
            }
        }

        await async_get_accounts(
            self.mocks["hass"],
            self.mocks["connection"],
            {"id": 1, "type": "spotcast/accounts"}
        )

    def test_correct_result_sent(self):
        try:
            self.mocks["connection"].send_result.assert_called_with(
                1,
                {
                    "total": 2,
                    "accounts": [
                        {
                            "entry_id": "12345",
                            "spotify_id": "id_a",
                            "spotify_name": "Name A",
                            "is_default": True,
                            "country": "CA"
                        },
                        {
                            "entry_id": "23456",
                            "spotify_id": "id_b",
                            "spotify_name": "Name B",
                            "is_default": False,
                            "country": "CA"
                        },
                    ]
                }
            )
        except AssertionError:
            self.fail()
