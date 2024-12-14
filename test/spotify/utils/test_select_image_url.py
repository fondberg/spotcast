"""Module to test the select image url function"""

from unittest import TestCase

from custom_components.spotcast.spotify.utils import select_image_url


class TestImageSelection(TestCase):

    def setUp(self):

        self.images = [
            {
                "height": 300,
                "url": "http://image.com/2",
                "width": 300
            },
            {
                "height": 640,
                "url": "http://image.com/1",
                "width": 640
            },
            {
                "height": 60,
                "url": "http://image.com/3",
                "width": 60
            }
        ]

        self.result = select_image_url(self.images)

    def test_correct_image_selected(self):
        self.assertEqual(self.result, "http://image.com/1")


class TestImageWithoutSize(TestCase):

    def setUp(self):

        self.images = [
            {
                "url": "http://image.com/2",
            },
            {
                "url": "http://image.com/1",
            },
            {
                "url": "http://image.com/3",
            }
        ]

        self.result = select_image_url(self.images)

    def test_correct_image_selected(self):
        self.assertEqual(self.result, "http://image.com/2")
