"""Module to test raise_on_invalid_filters function"""

from unittest import TestCase

from custom_components.spotcast.spotify.search_query import (
    SearchQuery,
    InvalidTagsError,
)


class TestValidTags(TestCase):

    def test_filter(self):

        tags = ["new", "hipster"]

        try:
            SearchQuery.raise_on_invalid_tags(tags)
        except InvalidTagsError:
            self.fail()


class TestInvalidTags(TestCase):

    def test_filter(self):

        tags = ["invalid"]

        with self.assertRaises(InvalidTagsError):
            SearchQuery.raise_on_invalid_tags(tags)
