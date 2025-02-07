"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.sensor.spotify_profile_sensor import (
    SpotifyProfileSensor,
    STATE_OK,
)


class TestSuccessfulUpdate(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.account = AsyncMock(spec=SpotifyAccount)
        self.sensor = SpotifyProfileSensor(self.account)

        self.account.name = "Dummy Account"
        self.account.entry_id = "12345"

        self.account.async_profile.return_value = {
            "id": "dummy_id",
            "explicit_content": {
                "filter_enabled": False,
                "filter_locked": False,
            },
            "followers": {
                "total": 10
            },
            "href": "http://locahost",
            "external_urls": {
                "spotify": "http://locahost"
            },
            "images": [
                {
                    "url": "http://locahost",
                    "height": 640,
                    "width": 640,
                }
            ]
        }
        await self.sensor.async_update()

    def test_profile_was_retrieved(self):
        try:
            self.account.async_profile.assert_called()
        except AssertionError:
            self.fail()

    def test_attribute_state_was_set_to_account_type(self):
        self.assertEqual(self.sensor.state, STATE_OK)

    def test_extra_attributes_saved(self):
        self.assertEqual(
            self.sensor.extra_state_attributes,
            {
                "id": "dummy_id",
                "filter_explicit_enabled": False,
                "filter_explicit_locked": False,
                "followers_count": 10,
                "entry_id": "12345",
            },
        )
