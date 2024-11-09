"""Module to test the async_devices function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from asyncio import get_running_loop

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestGettingDevices(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.account._profile = {
            "data": {
                "id": "dummy",
                "display_name": "Dummy Account"
            },
            "last_update": 0,
        }

        self.dummy_devices = {
            "devices": [
                {
                    'id': 'dummy_id_1',
                    'is_active': False,
                    'is_private_session': False,
                    'is_restricted': False,
                    'name': 'Dummy Device 1',
                    'supports_volume': True,
                    'type': 'Computer',
                    'volume_percent': 100
                },
                {
                    'id': 'dummy_id_2',
                    'is_active': False,
                    'is_private_session': False,
                    'is_restricted': False,
                    'name': 'Dummy Device 2',
                    'supports_volume': True,
                    'type': 'Computer',
                    'volume_percent': 100
                },
                {
                    'id': 'dummy_id_3',
                    'is_active': False,
                    'is_private_session': False,
                    'is_restricted': False,
                    'name': 'Dummy Device 3',
                    'supports_volume': True,
                    'type': 'Computer',
                    'volume_percent': 56
                }
            ]
        }

        loop = get_running_loop()

        self.mock_hass.async_add_executor_job\
            .return_value = loop.run_in_executor(
                None,
                lambda: self.dummy_devices
            )

        self.result = await self.account.async_devices()

    async def test_devices_returns_as_expected(self):
        self.assertEqual(self.result, self.dummy_devices["devices"])
