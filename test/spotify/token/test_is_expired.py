"""Module to test the is_expired method"""

from unittest import TestCase
from time import time

from custom_components.spotcast.spotify.token import SpotifyToken


class TestIsExpired(TestCase):

    def setUp(self):

        self.token = SpotifyToken("12345", time() + 1000)

    def test_no_access_token(self):
        self.token._access_token = None

        self.assertTrue(self.token.is_expired())

    def test_no_expiry_token(self):
        self.token.expires = None

        self.assertTrue(self.token.is_expired())

    def test_expired_time(self):
        self.token._access_token = "12345"
        self.token.expires = time() - 1000

        self.assertTrue(self.token.is_expired())


class TestIsNotExpired(TestCase):

    def setUp(self):
        self.token = SpotifyToken("12345", time() + 1000)

    def test_unexpired_token(self):
        self.assertFalse(self.token.is_expired())
