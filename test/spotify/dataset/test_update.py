"""Module to test the update function"""

from unittest import TestCase

from custom_components.spotcast.spotify.dataset import Dataset


class TestDataUpdate(TestCase):

    def setUp(self):
        self.dataset = Dataset("dummy", 30)
        self.data = {"foo", "bar"}
        self.dataset.update(self.data)

    def test_dataset_saved_new_data(self):
        self.assertEqual(self.dataset.data, self.data)

    def test_dataset_is_no_longer_expired(self):
        self.assertFalse(self.dataset.is_expired)

    def test_expires_at_was_changed(self):
        self.assertNotEqual(self.dataset.expires_at, 0)
