"""Module to test the is_expired_property"""

from unittest import TestCase
from time import time

from custom_components.spotcast.spotify.dataset import Dataset


class TestIsExpired(TestCase):

    def setUp(self):

        self.dataset = Dataset("dummy", 30)

    def test_last_refresh_too_old(self):
        self.dataset._data = {}
        self.assertTrue(self.dataset.is_expired())

    def test_data_missing(self):
        self.dataset.expires_at = time() + 9999
        self.assertTrue(self.dataset.is_expired())


class TestIsNotExpired(TestCase):

    def setUp(self):

        self.dataset = Dataset("dummy", 30)

    def test_recent_refresh(self):
        self.dataset.expires_at = time() + 9999
        self.dataset._data = {}
        self.assertFalse(self.dataset.is_expired())
