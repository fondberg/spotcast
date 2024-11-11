"""Module to test the entity_picture property"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast import SpotifyAccount
from custom_components.spotcast.sensor.spotify_profile_sensor import (
    SpotifyProfileSensor,
    STATE_OK,
    STATE_UNKNOWN,
)


class TestEntityPicture(TestCase):

    def setUp(self):
        self.account = MagicMock(spec=SpotifyAccount)
        self.account.image_link = "http://dummy-image.com/1"
        self.sensor = SpotifyProfileSensor(self.account)

    def test_image_link_returned_when_state_ok(self):
        self.sensor._attr_state = STATE_OK
        self.assertEqual(
            self.sensor.entity_picture,
            "http://dummy-image.com/1"
        )

    def test_image_none_returned_when_state_unknown(self):
        self.sensor._attr_state = STATE_UNKNOWN
        self.assertIsNone(self.sensor.entity_picture)
