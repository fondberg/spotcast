"""Module to test the data property"""

from unittest import TestCase
from time import time

from custom_components.spotcast.spotify.dataset import Dataset, ExpiredDatasetError


class TestDataFresh(TestCase):

    def setUp(self):
        self.dataset = Dataset("dummy", 30)
        self.dataset.expires_at = time() + 9999
        self.dataset._data = {"foo": "bar"}

    def test_data_is_returned(self):
        try:
            self.assertEqual(self.dataset.data, self.dataset._data)
        except ExpiredDatasetError:
            self.fail("The dataset should not be marked as expired")


class TestDataExpired(TestCase):

    def setUp(self):
        self.dataset = Dataset("dummy", 30)
        self.dataset._data = {"foo": "bar"}

    def test_data_is_returned(self):

        with self.assertRaises(ExpiredDatasetError):
            self.dataset.data
