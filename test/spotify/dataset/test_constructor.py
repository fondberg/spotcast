"""Module to test the dataset constructor"""

from unittest import TestCase

from custom_components.spotcast.spotify.dataset import (
    Dataset,
    Lock,
)


class TestDataretention(TestCase):

    def setUp(self):
        self.dataset = Dataset("dummy", 15)

    def test_name_is_retained(self):
        self.assertEqual(self.dataset.name, "dummy")

    def test_refresh_rate_is_retained(self):
        self.assertEqual(self.dataset.refresh_rate, 15)

    def test_data_is_initialised_to_none(self):
        self.assertIsNone(self.dataset._data)

    def test_expires_at_is_set_to_zero(self):
        self.assertEqual(self.dataset.expires_at, 0)

    def test_lock_is_created(self):
        self.assertIsInstance(self.dataset.lock, Lock)
