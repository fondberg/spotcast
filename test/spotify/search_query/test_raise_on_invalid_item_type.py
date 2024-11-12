"""Module to test raise_on_invalid_item_type function"""

from unittest import TestCase

from custom_components.spotcast.spotify.search_query import (
    SearchQuery,
    InvalidTagsError,
    InvalidItemTypeError,
)


class TestValidItemType(TestCase):

    def test_filter(self):

        try:
            SearchQuery.raise_on_invalid_item_type("track")
        except InvalidItemTypeError:
            self.fail()


class TestInvalidItemType(TestCase):

    def test_filter(self):

        with self.assertRaises(InvalidItemTypeError):
            SearchQuery.raise_on_invalid_item_type("invalid")
