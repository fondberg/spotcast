"""Module to test the read_only_dict_to_standard"""

from unittest import TestCase

from custom_components.spotcast.utils import (
    copy_to_dict,
    ReadOnlyDict,
)


class TestDictionaryConversion(TestCase):

    def setUp(self):

        self.expected = {
            "a": {
                "b": {"c": 1, "d": 3.1415},
                "e": [{"f": "foo"}, "bar"]
            },
            "g": True,
        }

        self.readonly = ReadOnlyDict(self.expected)
        self.result = copy_to_dict(self.readonly)

    def test_dictionary_properly_converted(self):
        self.assertEqual(self.result, self.expected)

    def test_main_dictionary_is_no_longer_read_only(self):
        self.assertIsInstance(self.result, dict)
        self.assertNotIsInstance(self.result, ReadOnlyDict)
