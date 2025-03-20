"""Module to test the query_from_url function"""

from unittest import TestCase

from custom_components.spotcast.utils import query_from_url

URL = (
    "/get_access_token?reason=transport&productType=web-player&totp=316647"
    "&totpServer=316647&totpVer=5&sTime=1742392418&cTime=1742392418"
    "&_authfailed=1"
)


class TestUrlParsing(TestCase):

    def setUp(self):
        self.url = URL
        self.result = query_from_url(self.url)

    def test_expected_query_returned(self):
        self.assertEqual(
            self.result,
            {
                "reason": "transport",
                "productType": "web-player",
                "totp": "316647",
                "totpServer": "316647",
                "totpVer": "5",
                "sTime": "1742392418",
                "cTime": "1742392418",
                "_authfailed": "1",
            }
        )


class TestEmptyString(TestCase):

    def setUp(self):
        self.url = ""
        self.result = query_from_url(self.url)

    def test_empty_dict_received(self):
        self.assertEqual(self.result, {})
