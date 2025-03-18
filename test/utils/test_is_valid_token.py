"""Module to test the is_valid_json function"""

from unittest import TestCase
import json

from custom_components.spotcast.utils import is_valid_json


class TestValidJson(TestCase):

    def test_is_valid(self):
        data = json.dumps({"foo": "bar"})
        self.assertTrue(is_valid_json(data))


class TestInvalidJson(TestCase):

    def test_is_valid(self):
        data = "foo"
        self.assertFalse(is_valid_json(data))
