"""Module to test the url to uri conversion"""

from unittest import TestCase

from custom_components.spotcast.spotify.utils import url_to_uri


class TestConversion(TestCase):

    def test_3_part_url(self):

        values = [
            "https://open.spotify.com/album/5l5m1hnH4punS1GQXgEi3T",
            "https://open.spotify.com/track/55mJleti2WfWEFNFcBduhc?si=89dc10a74e594be1",
            "https://open.spotify.com/artist/2yEwvVSSSUkcLeSTNyHKh8?si=4zoaG-AiRmaAgThLdsKqfA",
        ]

        expecteds = [
            "spotify:album:5l5m1hnH4punS1GQXgEi3T",
            "spotify:track:55mJleti2WfWEFNFcBduhc",
            "spotify:artist:2yEwvVSSSUkcLeSTNyHKh8",
        ]

        for value, expected in zip(values, expecteds):
            self.assertEqual(url_to_uri(value), expected)

    def test_user_specific_url(self):

        value = "https://open.spotify.com/user/1185903410/playlist/6YAnJeVC7tgOiocOG23Dd"
        expected = "spotify:user:1185903410:playlist:6YAnJeVC7tgOiocOG23Dd"

        self.assertEqual(url_to_uri(value), expected)


class TestUri(TestCase):

    def test_uris_are_skipped(self):

        values = [
            "spotify:album:5l5m1hnH4punS1GQXgEi3T",
            "spotify:track:55mJleti2WfWEFNFcBduhc",
            "spotify:artist:2yEwvVSSSUkcLeSTNyHKh8",
            "spotify:user:1185903410:playlist:6YAnJeVC7tgOiocOG23Dd",
        ]

        for value in values:
            self.assertEqual(url_to_uri(value), value)
