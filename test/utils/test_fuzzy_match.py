"""Module to test the fuzzy_match function"""

from unittest import TestCase

from custom_components.spotcast.utils import fuzzy_match, LowRatioError


class TestMatchFound(TestCase):

    def setUp(self):
        self.result = fuzzy_match(["foo", "bar", "baz"], "fou")

    def test_expected_result_found(self):
        self.assertEqual(self.result, "foo")


class TestNoMatchFound(TestCase):

    def test_error_raised_due_to_low_ratio(self):
        with self.assertRaises(LowRatioError):
            self.result = fuzzy_match(["foo", "bar", "baz"], "dummy")


class TestMatchWithKey(TestCase):

    def setUp(self):
        self.result = fuzzy_match(
            [
                {"name": "foo"},
                {"name": "bar"},
                {"name": "baz"},
            ],
            search="fou",
            key="name"
        )

    def test_expected_result_found(self):
        self.assertEqual(self.result, {"name": "foo"})
