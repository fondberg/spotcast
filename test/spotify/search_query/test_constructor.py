"""Module to test the constructor of the search_query object"""

from unittest import TestCase

from custom_components.spotcast.spotify.search_query import SearchQuery


class TestDataRetention(TestCase):

    def setUp(self):
        self.query = SearchQuery(
            "Finger To the Bone",
            item_type="track",
            filters={
                "artist": "Brown Bird",
                "album": "Salt For Salt"
            },
            tags=["new"]
        )

    def test_item_types_saved(self):
        self.assertEqual(self.query.item_type, "track")

    def test_search_saved(self):
        self.assertEqual(self.query.search, "Finger To the Bone")

    def test_filters_saved(self):
        self.assertEqual(
            self.query.filters,
            {"artist": "Brown Bird", "album": "Salt For Salt"}
        )

    def test_tags_saved(self):
        self.assertEqual(self.query.tags, ["new"])


class TestDefaults(TestCase):

    def setUp(self):
        self.query = SearchQuery(
            "Finger To the Bone",
            item_type="track",
        )

    def test_filters_saved(self):
        self.assertEqual(self.query.filters, {})

    def test_tags_saved(self):
        self.assertEqual(self.query.tags, [])
