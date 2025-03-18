"""Module to test the hex_to_bytes function"""

from unittest import TestCase

from custom_components.spotcast.crypto.utils import hex_to_bytes


class TestConversion(TestCase):

    def setUp(self):
        self.value = b"foo".hex()
        self.result = hex_to_bytes(self.value)

    def test_test(self):
        self.assertEqual(self.result, b"foo")
