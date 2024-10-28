"""Module to test the async_profile function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from asyncio import get_running_loop

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
    Spotify
)

from test.unit_utils import AsyncMock

TEST_MODULE = "custom_components.spotcast.spotify.account."


class TestProfileFetching(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.dummy_profile = {
            'country': 'CA',
            'display_name': 'Dummy User',
            'explicit_content': {
                'filter_enabled': False,
                'filter_locked': False
            },
            'external_urls': {
                'spotify': 'https://open.spotify.com/user/dummy_user'
            },
            'followers': {
                'href': None, 'total': 10
            },
            'href': 'https://api.spotify.com/v1/users/dummy_user',
            'id': 'dummy_user',
            'images': [
                {
                    'height': 300,
                    'url': 'https://localhost/?id=2',
                    'width': 300
                },
                {
                    'height': 64,
                    'url': 'https://localhost/?id=2',
                    'width': 64
                }
            ],
            'product': 'premium',
            'type': 'user',
            'uri': 'spotify:user:dummy_user'
        }

        loop = get_running_loop()

        self.mock_hass.async_add_executor_job\
            .return_value = loop.run_in_executor(
                None,
                lambda: self.dummy_profile
            )

        self.result = await self.account.async_profile()

    async def test_profile_received_as_expected(self):
        self.assertEqual(self.result, self.dummy_profile)

    async def test_name_was_set_in_account(self):
        self.assertEqual(self.account.name, self.dummy_profile["display_name"])


class TestProfileWithoutDisplayName(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.mock_hass = MagicMock(spec=HomeAssistant)

        self.account = SpotifyAccount(
            self.mock_hass,
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.dummy_profile = {
            'country': 'CA',
            'explicit_content': {
                'filter_enabled': False,
                'filter_locked': False
            },
            'external_urls': {
                'spotify': 'https://open.spotify.com/user/dummy_user'
            },
            'followers': {
                'href': None, 'total': 10
            },
            'href': 'https://api.spotify.com/v1/users/dummy_user',
            'id': 'dummy_user',
            'images': [
                {
                    'height': 300,
                    'url': 'https://localhost/?id=2',
                    'width': 300
                },
                {
                    'height': 64,
                    'url': 'https://localhost/?id=2',
                    'width': 64
                }
            ],
            'product': 'premium',
            'type': 'user',
            'uri': 'spotify:user:dummy_user'
        }

        loop = get_running_loop()

        self.mock_hass.async_add_executor_job\
            .return_value = loop.run_in_executor(
                None,
                lambda: self.dummy_profile
            )

        self.result = await self.account.async_profile()

    async def test_id_was_set_in_account(self):
        self.assertEqual(self.account.name, self.dummy_profile["id"])
