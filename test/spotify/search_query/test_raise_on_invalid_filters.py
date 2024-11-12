"""Module to test raise_on_invalid_filters function"""

from unittest import TestCase

from custom_components.spotcast.spotify.search_query import (
    SearchQuery,
    InvalidFilterError,
)


class TestValidFilters(TestCase):

    def test_filter(self):

        filters = {
            "artist": "Brown Bird"
        }

        try:
            SearchQuery.raise_on_invalid_filters(filters)
        except InvalidFilterError:
            self.fail()


class TestInvalidFilters(TestCase):

    def test_filter(self):

        filters = {
            "invalid": "Brown Bird"
        }

        with self.assertRaises(InvalidFilterError):
            SearchQuery.raise_on_invalid_filters(filters)
