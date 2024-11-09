"""Module to test the read_only_dict_to_standard"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.utils import (
    read_only_dict_to_standard,
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
        self.result = read_only_dict_to_standard(self.readonly)

    def test_dictionary_properly_converted(self):
        self.assertEqual(self.result, self.expected)

    def test_main_dictionary_is_no_longer_read_only(self):
        self.assertIsInstance(self.result, dict)
        self.assertNotIsInstance(self.result, ReadOnlyDict)
