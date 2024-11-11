"""Module to test the clean_extras method"""

from unittest import TestCase

from custom_components.spotcast.services.utils import clean_extras


class TestExtraCleanup(TestCase):

    def test_extras_are_cleanup(self):

        value = {
            "foo": True,
            "bar": 80,
        }

        expected = {"bar": 80}

        result = clean_extras(value, ["bar"])

        self.assertEqual(expected, result)
