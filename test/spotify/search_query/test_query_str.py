"""Module to test the query_str function"""

from unittest import TestCase

from custom_components.spotcast.spotify.search_query import SearchQuery


class TestQueryStrValue(TestCase):

    def setUp(self):

        self.query = SearchQuery(
            search="foo",
            item_type="track",
            filters={
                "artist": "bar",
                "album": "baz",
            },
            tags=["hipster"]
        )

    def test_expected_query_string_received(self):
        self.assertEqual(
            self.query.query_string,
            "foo artist:bar album:baz tag:hipster"
        )


class TestQueryWithEnptyFiltersAndTags(TestCase):

    def setUp(self):

        self.query = SearchQuery(
            search="foo",
            item_type="track",
        )

    def test_expected_query_string_received(self):
        self.assertEqual(
            self.query.query_string,
            "foo"
        )
