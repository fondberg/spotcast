"""Module to test the image_link property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
)


class TestImageLink(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "external": MagicMock(spec=OAuth2Session),
            "internal": MagicMock(spec=InternalSession),
        }

        self.account = SpotifyAccount(
            hass=self.mocks["hass"],
            external_session=self.mocks["external"],
            internal_session=self.mocks["internal"],
        )

        self.account._profile = {
            "country": "CA",
            "display_name": "Dummy User",
            "email": "dummyemail@gmail.com",
            "explicit_content": {
                "filter_enabled": False,
                "filter_locked": False
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/user/dummy_user"
            },
            "followers": {
                "href": None,
                "total": 10
            },
            "href": "https://api.spotify.com/v1/users/dummy_user",
            "id": "dummy_user",
            "images": [
                {
                    "url": "https://dummy-1.link",
                    "height": 300,
                    "width": 300
                },
                {
                    "url": "https://dummy-2.link",
                    "height": 64,
                    "width": 64
                }
            ],
            "product": "premium",
            "type": "user",
            "uri": "spotify:user:dummy_user"
        }

    def test_proper_link_returned(self):
        self.assertEqual(self.account.image_link, "https://dummy-1.link")
