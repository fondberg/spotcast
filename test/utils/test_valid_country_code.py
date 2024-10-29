"""Module to test the valid_country_code function"""

from unittest import TestCase

from voluptuous import Invalid

from custom_components.spotcast.utils import valid_country_code


class TestValidCountryCodes(TestCase):

    def test_valid_country_code(self):
        self.assertEqual(valid_country_code("CA"), "CA")

    def test_country_code_coverted_to_upper(self):
        self.assertEqual(valid_country_code("ca"), "CA")


class TestInvalidCountryCodes(TestCase):

    def test_none_string_code(self):
        with self.assertRaises(Invalid):
            valid_country_code(42)

    def test_none_2_char_code(self):
        with self.assertRaises(Invalid):
            valid_country_code("Canada")
